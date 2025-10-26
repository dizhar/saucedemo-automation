#!/usr/bin/env python3
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import glob
import re
import argparse
import shutil
import os

# =============================================================================
# Utility Functions
# =============================================================================

def clean_allure_results():
    """Clean previous allure results and reports."""
    for path in ['allure-results', 'allure-report', 'allure-results-merged']:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"🧹 Cleaned previous {path}")


def remove_empty_allure_files(results_dir):
    """Remove any empty or corrupted Allure JSON files."""
    if not os.path.exists(results_dir):
        return
    removed = 0
    for root, _, files in os.walk(results_dir):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                if os.path.getsize(full_path) == 0:
                    os.remove(full_path)
                    removed += 1
                    print(f"⚠️ Removed empty Allure file: {f}")
            except OSError:
                continue
    if removed:
        print(f"✅ Removed {removed} empty result files.")


def merge_allure_results(base_dir='allure-results', merged_dir='reports/allure-results'):
    """Merge multiple parallel Allure result directories into one."""
    if not os.path.exists(base_dir):
        print("❌ No allure-results directory found to merge.")
        return None

    os.makedirs(merged_dir, exist_ok=True)

    os.makedirs(merged_dir, exist_ok=True)
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.json') or f.endswith('.txt') or f.endswith('.xml'):
                src = os.path.join(root, f)
                dst = os.path.join(merged_dir, f)
                try:
                    shutil.copy(src, dst)
                except Exception as e:
                    print(f"⚠️ Failed to copy {f}: {e}")

    print("✅ Merged Allure results into", merged_dir)
    remove_empty_allure_files(merged_dir)
    return merged_dir


def generate_allure_report(results_dir='allure-results', serve=False):
    """Generate or serve the Allure report."""
    print("\n" + "="*80)
    print("📊 Generating Allure Report...")
    print("="*80)

    if not os.path.exists(results_dir):
        print("❌ No Allure results found to generate report.")
        return False

    if not shutil.which('allure'):
        print("❌ Allure command not found!")
        print("Please install Allure CLI:")
        print("  macOS: brew install allure")
        print("  Docs: https://docs.qameta.io/allure/#_installing_a_commandline")
        return False

    try:
        if serve:
            print("🚀 Opening Allure report in browser...")
            subprocess.run(['allure', 'serve', results_dir], check=True)
        else:
            subprocess.run(['allure', 'generate', results_dir, '--clean', '-o', 'reports/allure-report'], check=True)
            print("✅ Report generated successfully!")
            print("📁 Location: allure-report/index.html")
            print("\nTo open:")
            print("  allure open allure-report")
            print("  or open allure-report/index.html in your browser")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating Allure report: {e}")
        return False


# =============================================================================
# Test Execution
# =============================================================================

def run_feature(feature_file, use_allure=False):
    """Run a single feature file."""
    print(f"Running: {feature_file}")
    cmd = ['behave', feature_file, '--no-capture']

    if use_allure:
        pid_dir = f'allure-results/{os.getpid()}'
        os.makedirs(pid_dir, exist_ok=True)
        cmd.extend(['--format', 'allure_behave.formatter:AllureFormatter', '--outfile', pid_dir])

    result = subprocess.run(cmd, text=True)
    return {'name': feature_file, 'returncode': result.returncode}


def get_scenarios(feature_file):
    """Extract scenario names and line numbers from feature file."""
    scenarios = []
    try:
        with open(feature_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if re.match(r'^\s*Scenario(\sOutline)?:', line):
                    scenario_name = line.strip()
                    scenarios.append({'name': f"{feature_file}:{line_num} - {scenario_name}", 'file': feature_file, 'line': line_num})
    except Exception as e:
        print(f"Error reading {feature_file}: {e}")
    return scenarios


def run_scenario(scenario_info, use_allure=False):
    """Run a single scenario by line number."""
    print(f"Running: {scenario_info['name']}")
    cmd = ['behave', f"{scenario_info['file']}:{scenario_info['line']}", '--no-capture']

    if use_allure:
        pid_dir = f'allure-results/{os.getpid()}'
        os.makedirs(pid_dir, exist_ok=True)
        cmd.extend(['--format', 'allure_behave.formatter:AllureFormatter', '--outfile', pid_dir])

    result = subprocess.run(cmd, text=True)
    return {'name': scenario_info['name'], 'returncode': result.returncode}


# =============================================================================
# Main Runner
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Run Behave tests in parallel with optional Allure reporting')
    parser.add_argument('--mode', choices=['features', 'scenarios'], default='features', help='Run by features (default) or by scenarios')
    parser.add_argument('--file', help='Specific feature file to run scenarios from')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--report', action='store_true', help='Generate Allure report after tests')
    parser.add_argument('--serve', action='store_true', help='Generate and serve Allure report in browser (implies --report)')
    parser.add_argument('--clean', action='store_true', help='Clean previous allure results before running')
    args = parser.parse_args()

    if args.serve:
        args.report = True

    if args.clean:
        clean_allure_results()

    if args.report:
        try:
            import allure_behave
        except ImportError:
            print("❌ allure-behave not installed! Run: pip install allure-behave")
            sys.exit(1)

    # Determine test mode
    failed, passed = [], []
    if args.mode == 'scenarios':
        feature_files = [args.file] if args.file else glob.glob('features/*.feature')
        all_scenarios = [s for f in feature_files for s in get_scenarios(f)]

        if not all_scenarios:
            print("No scenarios found!")
            sys.exit(1)

        print(f"Found {len(all_scenarios)} scenarios")
        print("="*80)

        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(run_scenario, s, args.report): s for s in all_scenarios}
            for future in as_completed(futures):
                result = future.result()
                if result['returncode'] == 0:
                    passed.append(result['name'])
                    print(f"✅ PASSED: {result['name']}")
                else:
                    failed.append(result['name'])
                    print(f"❌ FAILED: {result['name']}")

    else:
        feature_files = glob.glob('features/*.feature')
        if not feature_files:
            print("No feature files found!")
            sys.exit(1)

        print(f"Found {len(feature_files)} feature files")
        print("="*80)

        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(run_feature, f, args.report): f for f in feature_files}
            for future in as_completed(futures):
                result = future.result()
                if result['returncode'] == 0:
                    passed.append(result['name'])
                    print(f"✅ PASSED: {result['name']}")
                else:
                    failed.append(result['name'])
                    print(f"❌ FAILED: {result['name']}")

    # Summary
    print("="*80)
    print(f"✅ Passed: {len(passed)}")
    print(f"❌ Failed: {len(failed)}")
    if failed:
        print("\nFailed items:")
        for f in failed:
            print(f"  - {f}")
    else:
        print("\n🎉 All tests passed!")

    # Generate Allure report
    if args.report:
        merged_dir = merge_allure_results()
        if merged_dir:
            generate_allure_report(results_dir=merged_dir, serve=args.serve)

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()