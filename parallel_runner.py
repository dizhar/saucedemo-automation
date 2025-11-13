#!/usr/bin/env python3
"""
Parallel Test Runner for Behave
Runs scenarios in parallel across multiple processes
"""

import subprocess
import sys
import os
import json
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil
import signal
import atexit


# Global process tracking for cleanup
_active_processes = []


def cleanup_processes():
    """Clean up any remaining test processes"""
    for process in _active_processes:
        try:
            if process.poll() is None:  # Still running
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        except Exception:
            pass
    _active_processes.clear()


# Register cleanup handlers
atexit.register(cleanup_processes)
signal.signal(signal.SIGTERM, lambda s, f: cleanup_processes())
signal.signal(signal.SIGINT, lambda s, f: cleanup_processes())


class ParallelBehaveRunner:
    """Runs Behave scenarios in parallel"""
    
    def __init__(self, workers=3, tags=None, serve_report=False):
        self.workers = workers
        self.tags = tags
        self.serve_report = serve_report
        self.results = []
    
    def get_all_scenarios(self):
        """Get list of all scenarios by parsing dry-run output"""
        cmd = ['behave', '--dry-run', '--no-summary', '--no-capture', '--no-color']
        
        if self.tags:
            cmd.extend(['--tags', self.tags])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        scenarios = []
        current_feature = None
        
        # Combine stdout and stderr
        output = result.stdout + result.stderr
        
        for line in output.splitlines():
            # Match feature file line: "Feature: Login Functionality  # features/login.feature:1"
            if 'Feature:' in line and '#' in line and 'features/' in line:
                import re
                match = re.search(r'#\s+(features/[^:]+):', line)
                if match:
                    current_feature = match.group(1)
            
            # Match scenario line: "  Scenario: Successful login  # features/login.feature:12"
            # or: "  Scenario Outline: Login with data  # features/login.feature:25"
            if ('Scenario:' in line or 'Scenario Outline:' in line) and '#' in line:
                import re
                # Extract file:line from comment
                match = re.search(r'#\s+(features/[^:]+):(\d+)', line)
                if match:
                    feature_file = match.group(1)
                    line_num = match.group(2)
                    location = f"{feature_file}:{line_num}"
                    
                    # Avoid duplicates
                    if location not in scenarios:
                        scenarios.append(location)
                        print(f"  Found: {location}", flush=True)
        
        print(f"\n✅ Total scenarios found: {len(scenarios)}\n", flush=True)
        return scenarios
    
    def run_scenario(self, scenario_location, worker_id):
        """Run a single scenario"""
        print(f"[Worker {worker_id}] Running: {scenario_location}", flush=True)
        
        # Create worker-specific output directory
        worker_results_dir = f"reports/json-results/worker-{worker_id}"
        os.makedirs(worker_results_dir, exist_ok=True)
        
        env = os.environ.copy()
        env['WORKER_ID'] = str(worker_id)
        
        # Ensure all environment variables are passed
        for key in ['SELENIUM_REMOTE_URL', 'SELENIUM_REMOTE', 'HEADLESS', 
                    'IMPLICIT_WAIT', 'PAGE_LOAD_TIMEOUT', 'DEFAULT_TIMEOUT']:
            if key in os.environ:
                env[key] = os.environ[key]
        
        # Use JSON output instead of Allure (Allure has threading issues)
        json_output = f"{worker_results_dir}/result.json"
        
        cmd = [
            'behave',
            scenario_location,
            '--no-capture',
            '--format', 'json',
            '-o', json_output,
            '--no-color'
        ]
        
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Track process for cleanup
        _active_processes.append(process)
        
        try:
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout per scenario
            returncode = process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            returncode = -1
            print(f"⏱️  Timeout: {scenario_location}", flush=True)
        finally:
            # Remove from tracking
            if process in _active_processes:
                _active_processes.remove(process)
        
        status = "✅" if returncode == 0 else "❌"
        print(f"{status} {scenario_location}", flush=True)
        
        return {
            'scenario': scenario_location,
            'worker': worker_id,
            'success': returncode == 0,
            'returncode': returncode,
            'stdout': stdout,
            'stderr': stderr
        }
    
    def run_parallel(self):
        """Execute all scenarios in parallel"""
        # Get all scenarios
        scenarios = self.get_all_scenarios()
        
        if not scenarios:
            print("❌ No scenarios found!")
            return []
        
        print(f"📋 Found {len(scenarios)} scenarios")
        print(f"🚀 Running with {self.workers} workers...")
        print("")

        # Clean ALL old results before starting
        json_results_dir = Path("reports/json-results")
        if json_results_dir.exists():
            shutil.rmtree(json_results_dir, ignore_errors=True)
        json_results_dir.mkdir(parents=True, exist_ok=True)
        
        allure_results_dir = Path("reports/allure-results")
        if allure_results_dir.exists():
            print("🧹 Cleaning old Allure results...", flush=True)
            shutil.rmtree(allure_results_dir, ignore_errors=True)
        allure_results_dir.mkdir(parents=True, exist_ok=True)
        
        
        # Run scenarios in parallel
        results = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {}
            
            for i, scenario in enumerate(scenarios):
                worker_id = (i % self.workers) + 1
                future = executor.submit(self.run_scenario, scenario, worker_id)
                futures[future] = scenario
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    
                except Exception as e:
                    print(f"❌ Error running {futures[future]}: {e}", flush=True)
        
        # Cleanup any remaining processes
        cleanup_processes()
        
        return results
    
    def generate_allure_results(self):
        """Generate Allure results by running all features with Allure formatter"""
        print("\n🔄 Generating Allure results...", flush=True)
        
        allure_results_dir = Path("reports/allure-results")
        
        # Get unique feature files - try Docker path first, then local
        features_dir = Path("/app/features")
        if not features_dir.exists():
            features_dir = Path("features")
        
        if not features_dir.exists():
            print("⚠️  Features directory not found", flush=True)
            return
        
        feature_files = list(features_dir.glob("*.feature"))
        
        if not feature_files:
            print("⚠️  No feature files found", flush=True)
            return
        
        print(f"Found {len(feature_files)} feature files to process", flush=True)
        
        # Run each feature file with Allure formatter
        for feature_file in feature_files:
            try:
                print(f"  Processing {feature_file.name}...", flush=True)
                
                allure_cmd = [
                    'behave',
                    str(feature_file),
                    '--no-capture',
                    '--format', 'allure_behave.formatter:AllureFormatter',
                    '-o', str(allure_results_dir),
                    '--no-color'
                ]
                
                result = subprocess.run(
                    allure_cmd,
                    capture_output=True,
                    timeout=120,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"    ⚠️  Non-zero exit code for {feature_file.name}", flush=True)
                        
            except subprocess.TimeoutExpired:
                print(f"  ⏱️  Timeout processing {feature_file.name}", flush=True)
            except Exception as e:
                print(f"  ⚠️  Error processing {feature_file.name}: {e}", flush=True)
        
        # Check if any results were generated
        result_files = list(allure_results_dir.glob("*-result.json"))
        print(f"✅ Generated {len(result_files)} Allure result files", flush=True)
    
    def serve_allure_report(self):
        """Serve Allure report using allure serve command"""
        print("\n🌐 Starting Allure report server...", flush=True)
        print("Press Ctrl+C to stop the server", flush=True)
        
        try:
            subprocess.run([
                'allure',
                'serve',
                'reports/allure-results'
            ])
        except KeyboardInterrupt:
            print("\n👋 Allure server stopped", flush=True)
        except FileNotFoundError:
            print("⚠️  Allure command not found. Install with: brew install allure", flush=True)
    
    def print_summary(self, results):
        """Print test execution summary"""
        passed = sum(1 for r in results if r['success'])
        failed = len(results) - passed
        
        print("")
        print("=" * 80)
        print(f"📊 Test Results Summary")
        print("=" * 80)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total:  {len(results)}")
        print("=" * 80)
        
        if not self.serve_report:
            print("")
            print("📊 To view Allure report, run:")
            print(f"   allure serve reports/allure-results")
            print("")
        
        return failed == 0


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Behave tests in parallel')
    parser.add_argument('--workers', type=int, default=3, help='Number of parallel workers')
    parser.add_argument('--tags', type=str, help='Behave tags to filter scenarios')
    parser.add_argument('--serve', action='store_true', help='Serve Allure report after tests complete')
    
    args = parser.parse_args()
    
    runner = ParallelBehaveRunner(workers=args.workers, tags=args.tags, serve_report=args.serve)
    
    try:
        results = runner.run_parallel()
        
        if results:
            # Generate Allure results
            print("\n📊 Generating Allure files...", flush=True)
            try:
                runner.generate_allure_results()
            except Exception as e:
                print(f"⚠️  Could not generate Allure results: {e}", flush=True)
            
            success = runner.print_summary(results)
            
            # Serve report if requested
            if args.serve:
                runner.serve_allure_report()
            
            sys.exit(0 if success else 1)
        else:
            print("❌ No tests were run!")
            sys.exit(1)
    finally:
        # Ensure cleanup on exit
        cleanup_processes()


if __name__ == '__main__':
    main()