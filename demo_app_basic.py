"""
🎬 SauceDemo Test Automation - Live Demo with Browser Streaming
===============================================================
Option 2: Local - Generate Static Allure Report
- Uses `allure generate` to create static HTML into <reports>/allure-static
- Serves it via a lightweight local HTTP server (default http://localhost:8666)

FIXES:
1. UI remains interactive while tests are running (no blocking rerun)
2. Stop button properly terminates tests
3. Compatible with older Streamlit versions (no fragment API needed)
4. Automatically switches to Allure Report tab and generates report when tests complete
5. FIXED: Properly resets test results to 0 when starting new test run
6. Parallel Workers slider: 1-5 range, disabled during test runs
7. Removed Parallel Execution checkbox - workers determined by slider value
"""

import streamlit as st
import subprocess
import threading
import time
import os
import queue
import shutil
import socket
from datetime import datetime
from typing import Optional
from shutil import which

# ---------- Page configuration ----------
st.set_page_config(
    page_title="SauceDemo Test Automation Demo",
    page_icon="🧪",
    layout="wide"
)

# ---------- Path helpers (ALWAYS absolute) ----------
def _project_root() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def get_reports_base_dir() -> str:
    # Always absolute so CWD doesn't matter
    if os.getenv('SELENIUM_REMOTE_URL'):
        base = "/app/reports"
    else:
        base = os.path.join(_project_root(), "reports")
    os.makedirs(base, exist_ok=True)
    return base

def allure_paths():
    base = get_reports_base_dir()
    results = os.path.join(base, "allure-results")
    static = os.path.join(base, "allure-static")
    return results, static, base

# ---------- Simple local HTTP server for static files ----------
def _get_free_port(preferred: int = 8666) -> int:
    """Return preferred if available; otherwise any free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", preferred))
            s.close()
            return preferred
        except OSError as e:
            # In Docker, we MUST use the exposed port
            if os.getenv('SELENIUM_REMOTE_URL'):
                print(f"[ERROR] Port {preferred} not available in Docker: {e}", flush=True)
                return preferred
            else:
                s.bind(("127.0.0.1", 0))
                port = s.getsockname()[1]
                s.close()
                return port

def start_static_server_once(serve_dir: str, preferred_port: int = 8666):
    """
    Start a simple HTTP server (in a thread) to serve `serve_dir`.
    Only starts once per session.
    Binds to 0.0.0.0 to be reachable even when proxied (e.g., Docker).
    """
    # In Docker, FORCE port 8666 (which is exposed)
    if os.getenv('SELENIUM_REMOTE_URL'):
        port = 8666
    else:
        port = _get_free_port(preferred_port)
    
    if 'static_server' in st.session_state and st.session_state.static_server.get('running'):
        # Already running, check if it's on the right port
        meta = st.session_state.static_server
        existing_port = meta.get('port')
        if existing_port == port:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=0.3):
                    return  # Server is running and accessible on correct port
            except Exception:
                pass
        # Wrong port or dead server, clear state
        st.session_state.static_server = {'running': False}

    import http.server
    import socketserver
    from functools import partial

    Handler = partial(http.server.SimpleHTTPRequestHandler, directory=serve_dir)

    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    def _serve():
        try:
            httpd = ReusableTCPServer(("0.0.0.0", port), Handler)
            st.session_state.static_server = {'running': True, 'port': port, 'dir': serve_dir}
            print(f"[Static Server] Started on 0.0.0.0:{port}", flush=True)
            httpd.serve_forever()
        except Exception as e:
            print(f"[Static Server] Error: {e}", flush=True)
            st.session_state.static_server = {'running': False, 'error': str(e)}
            return

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()
    time.sleep(0.5)
    
    # Verify it started
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            print(f"[Static Server] Verified running on port {port}", flush=True)
            st.session_state.static_server = {'running': True, 'port': port, 'dir': serve_dir, 'thread': thread}
    except Exception as e:
        print(f"[Static Server] Failed to verify: {e}", flush=True)
        st.session_state.static_server = {'running': False, 'error': f"Failed to bind: {e}"}

# ---------- Allure static generation ----------
def get_allure_test_counts() -> dict:
    """
    Read Allure test counts using multiple methods for accuracy.
    Priority: 1) widgets/summary.json, 2) Parse result files
    Returns dict with 'passed', 'failed', 'total' keys.
    """
    results_dir, static_dir, _ = allure_paths()
    
    # Method 1: Try to read from generated Allure report's summary
    summary_path = os.path.join(static_dir, 'widgets', 'summary.json')
    if os.path.exists(summary_path):
        try:
            import json
            with open(summary_path, 'r') as f:
                summary = json.load(f)
            
            # Allure summary has 'statistic' object with counts
            stats = summary.get('statistic', {})
            passed = stats.get('passed', 0)
            failed = stats.get('failed', 0) + stats.get('broken', 0)
            total = stats.get('total', passed + failed)
            
            print(f"[Allure] Read from summary.json: {total} tests ({passed} passed, {failed} failed)", flush=True)
            return {'passed': passed, 'failed': failed, 'total': total}
        except Exception as e:
            print(f"[Allure] Could not read summary.json: {e}", flush=True)
    
    # Method 2: Parse result files (fallback)
    if not os.path.exists(results_dir):
        return {'passed': 0, 'failed': 0, 'total': 0}
    
    import json
    import glob
    
    passed = 0
    failed = 0
    
    # Only read test result files (end with -result.json)
    result_files = glob.glob(os.path.join(results_dir, '*-result.json'))
    
    for filepath in result_files:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Skip if this doesn't look like a test result
            if 'name' not in data or 'status' not in data:
                continue
            
            name = data.get('name', '').lower()
            full_name = data.get('fullName', '').lower()
            
            # Filter out fixtures and hooks - only count actual test scenarios
            # Behave/Allure creates result files for before/after hooks
            skip_keywords = ['before_', 'after_', 'setup', 'teardown', 'fixture']
            if any(keyword in name for keyword in skip_keywords):
                continue
            if any(keyword in full_name for keyword in skip_keywords):
                continue
            
            # Additional check: Real test cases usually have 'testCaseId'
            if 'testCaseId' not in data and 'historyId' not in data:
                continue
            
            # Count by status
            status = data.get('status', '').lower()
            
            if status == 'passed':
                passed += 1
            elif status in ('failed', 'broken'):
                failed += 1
                
        except Exception as e:
            print(f"[Allure] Error reading {filepath}: {e}", flush=True)
            continue
    
    total = passed + failed
    print(f"[Allure] Counted {total} actual test cases ({passed} passed, {failed} failed) from {len(result_files)} result files", flush=True)
    return {'passed': passed, 'failed': failed, 'total': total}

def allure_generate_static() -> tuple[bool, str]:
    """
    Run `allure generate <results> -o <static> --clean`.
    Returns (ok, message).
    """
    results_dir, static_dir, _ = allure_paths()

    if not os.path.exists(results_dir) or not os.listdir(results_dir):
        return False, f"No Allure results found in: {results_dir}"

    # Ensure static dir exists cleanly
    try:
        if os.path.exists(static_dir):
            shutil.rmtree(static_dir, ignore_errors=True)
        os.makedirs(static_dir, exist_ok=True)
    except Exception as e:
        return False, f"Failed to prepare static dir: {e}"

    if which("allure") is None:
        return False, (
            "Allure CLI not found in PATH.\n"
            "Install it and try again:\n"
            " - macOS: brew install allure\n"
            " - Linux: https://github.com/allure-framework/allure2\n"
        )

    cmd = ["allure", "generate", results_dir, "-o", static_dir, "--clean"]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if proc.returncode != 0:
            return False, f"`allure generate` failed (exit {proc.returncode}):\n{proc.stdout}"
        return True, f"Static report generated at: {static_dir}\n\n{proc.stdout}"
    except Exception as e:
        return False, f"Error running `allure generate`: {e}"

# ---------- Selenium node management ----------
def stop_selenium_nodes():
    """Stop Selenium node containers to save resources"""
    try:
        result = subprocess.run(
            [
                'docker-compose', '-f', 'docker-compose.demo.yml', 'stop',
                'selenium-chrome-1',
                'selenium-chrome-2',
                'selenium-chrome-3',
                'selenium-chrome-4',  # 🔹 NEW
                'selenium-chrome-5',  # 🔹 NEW
            ],
            cwd=_project_root(),
            capture_output=True,
            text=True
        )
        print(f"[Selenium] Stop nodes: {result.stdout}", flush=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[Selenium] Error stopping nodes: {e}", flush=True)
        return False


def start_selenium_nodes(num_workers: int = 3):
    """Start only the required number of Selenium node containers"""
    try:
        # Determine which nodes to start based on worker count
        nodes_to_start = []
        for i in range(1, min(num_workers, 5) + 1):  # 🔺 was 3, now 5
            nodes_to_start.append(f'selenium-chrome-{i}')
        
        if not nodes_to_start:
            nodes_to_start = ['selenium-chrome-1']  # At least start one node
        
        result = subprocess.run(
            ['docker-compose', '-f', 'docker-compose.demo.yml', 'start'] + nodes_to_start,
            cwd=_project_root(),
            capture_output=True,
            text=True
        )
        print(f"[Selenium] Start nodes ({len(nodes_to_start)}): {result.stdout}", flush=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[Selenium] Error starting nodes: {e}", flush=True)
        return False

# ---------- Test runner ----------
class TestRunner:
    """Handles test execution and output streaming"""
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.output_queue = queue.Queue()
        self.is_running = False
        self.results = {'passed': 0, 'failed': 0, 'total': 0}

    def stop_tests(self):
        """Stop running tests and ensure proper cleanup"""
        if self.process:
            print("[TestRunner] Stopping tests...", flush=True)
            try:
                # Send SIGTERM first
                self.process.terminate()
                # Wait up to 5 seconds for graceful shutdown
                self.process.wait(timeout=5)
                print("[TestRunner] Tests stopped gracefully", flush=True)
            except subprocess.TimeoutExpired:
                # Force kill if still running
                print("[TestRunner] Force killing process", flush=True)
                self.process.kill()
                self.process.wait()
            except Exception as e:
                print(f"[TestRunner] Error stopping: {e}", flush=True)
            finally:
                self.process = None
        
        self.is_running = False
        # Clear any remaining output
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break

    def check_if_finished(self):
        """Check if test process has finished"""
        if self.process and self.process.poll() is not None:
            self.is_running = False
            self.process = None
            return True
        return False

    def stream_output(self, process):
        """Stream process output to queue"""
        try:
            for line in iter(process.stdout.readline, ''):
                if line:
                    line_stripped = line.strip()
                    self.output_queue.put(line_stripped)
                    # DON'T parse results during execution - sidebar stays at 0
                    # Results will be loaded from Allure after report generation
                    # self.parse_results(line_stripped)
        except Exception as e:
            print(f"[TestRunner] Output streaming error: {e}", flush=True)
        finally:
            process.stdout.close()
            self.is_running = False
            self.process = None
            # Signal that we're done
            self.output_queue.put("__TESTS_COMPLETED__")

    def parse_results(self, line):
        """Parse test results from behave/parallel runner output"""
        import re
        if "✅ Passed:" in line:
            m = re.search(r'✅ Passed:\s*(\d+)', line)
            if m:
                self.results['passed'] = int(m.group(1))
                return
        if "❌ Failed:" in line:
            m = re.search(r'❌ Failed:\s*(\d+)', line)
            if m:
                self.results['failed'] = int(m.group(1))
                return
        if "📊 Total:" in line:
            m = re.search(r'📊 Total:\s*(\d+)', line)
            if m:
                self.results['total'] = int(m.group(1))
                return

        # Fallback: behave summary
        low = line.lower()
        if "scenario" in low and "passed" in low:
            try:
                passed = re.findall(r'(\d+)\s+scenario[s]?\s+passed', low)
                if passed:
                    self.results['passed'] = int(passed[0])
                failed = re.findall(r'(\d+)\s+failed', low)
                if failed:
                    self.results['failed'] = int(failed[0])
                self.results['total'] = self.results['passed'] + self.results['failed']
            except Exception:
                pass

    def run_tests(self, tags=None):
        """Run behave tests with optional parallel execution"""
        self.is_running = True
        # CRITICAL: Reset results at the START of test execution
        self.results = {'passed': 0, 'failed': 0, 'total': 0}

        # Clean old Allure results
        results_dir, _, _ = allure_paths()
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir, ignore_errors=True)
        os.makedirs(results_dir, exist_ok=True)

        workers = int(os.getenv('PARALLEL_WORKERS', '1'))

        if workers > 1:
            # NOTE: Ensure your parallel_runner.py passes the Allure formatter too.
            cmd = ['python', 'parallel_runner.py', '--workers', str(workers)]
            if tags:
                cmd.extend(['--tags', tags])
        else:
            # SEQUENTIAL mode - use both plain and Allure formatters for better compatibility
            # Using multiple formatters helps avoid context issues with Allure
            cmd = [
                'behave',
                '-f', 'plain',
                '-f', 'allure_behave.formatter:AllureFormatter',
                '-o', results_dir,
                '--no-capture',
                '--no-capture-stderr'
            ]
            if tags:
                cmd.extend(['--tags', tags])

        env = os.environ.copy()
        env['HEADLESS'] = 'false'
        if os.getenv('SELENIUM_REMOTE_URL'):
            env['SELENIUM_REMOTE'] = 'true'

        # Run from the project root so `features/` is found
        project_root = _project_root()

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            cwd=project_root  # <<< important
        )
        thread = threading.Thread(target=self.stream_output, args=(self.process,), daemon=True)
        thread.start()
        return self.process

# ---------- Process output updates ----------
def process_output_updates():
    """Process any new output from the test runner queue"""
    test_runner = st.session_state.test_runner
    vnc_available = os.getenv('SELENIUM_REMOTE_URL') is not None
    
    # Drain queue and check for completion
    tests_completed = False
    new_lines = []
    
    # Process up to 50 lines at once to avoid blocking
    for _ in range(50):
        try:
            line = test_runner.output_queue.get_nowait()
            if line == "__TESTS_COMPLETED__":
                tests_completed = True
            else:
                new_lines.append(line)
        except queue.Empty:
            break
    
    # Add new lines to output
    if new_lines:
        st.session_state.output_lines.extend(new_lines)
        # Keep only last 1000 lines to prevent memory issues
        if len(st.session_state.output_lines) > 1000:
            st.session_state.output_lines = st.session_state.output_lines[-1000:]
    
    # Handle test completion
    if tests_completed and st.session_state.tests_were_running:
        st.toast("✅ Tests completed! Generating Allure report...", icon="🎉")
        if vnc_available:
            stop_selenium_nodes()
        st.session_state.tests_were_running = False
        test_runner.is_running = False
        
        # DON'T load results here - the JSON files may be stale from previous runs
        # Results will be loaded AFTER Allure report generation in the tab handler
        
        # AUTOMATIC: Switch to Allure Report tab and generate report
        st.session_state.active_tab = "📊 Allure Report"
        st.session_state.auto_generate_report = True
        
        return True  # Signal completion
    
    # Also check if process finished (backup detection)
    if test_runner.check_if_finished() and st.session_state.tests_were_running:
        st.toast("✅ Tests finished! Generating Allure report...", icon="🎉")
        if vnc_available:
            stop_selenium_nodes()
        st.session_state.tests_were_running = False
        
        # DON'T load results here - the JSON files may be stale from previous runs
        # Results will be loaded AFTER Allure report generation in the tab handler
        
        # AUTOMATIC: Switch to Allure Report tab and generate report
        st.session_state.active_tab = "📊 Allure Report"
        st.session_state.auto_generate_report = True
        
        return True  # Signal completion
    
    return False  # Still running

# ---------- App ----------
def main():
    """Main Streamlit application"""

    # Session state
    if 'test_runner' not in st.session_state:
        st.session_state.test_runner = TestRunner()
    if 'output_lines' not in st.session_state:
        st.session_state.output_lines = []
    if 'parallel_workers' not in st.session_state:
        st.session_state.parallel_workers = 3
    if 'report_refresh_token' not in st.session_state:
        st.session_state.report_refresh_token = 0
    if 'tests_were_running' not in st.session_state:
        st.session_state.tests_were_running = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "🌐 Live Browser View"
    if 'auto_generate_report' not in st.session_state:
        st.session_state.auto_generate_report = False

    test_runner = st.session_state.test_runner
    vnc_available = os.getenv('SELENIUM_REMOTE_URL') is not None

    # Process output updates (non-blocking)
    tests_completed = process_output_updates()

    # Header
    st.title("🧪 SauceDemo Test Automation - Live Demo")
    st.markdown("### Watch automated tests run in real-time!")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        test_suite = st.selectbox(
            "Test Suite",
            ["Smoke Tests (@smoke)", "Login Tests (@login)", "All Tests"],
            key='test_suite'
        )

        st.divider()
        workers = st.slider(
            "Parallel Workers", 
            2, 5, 3, 
            help="Number of parallel test workers (2–5)",
            disabled=test_runner.is_running
        )
        st.session_state.parallel_workers = workers
        os.environ['PARALLEL_WORKERS'] = str(workers)
        parallel_enabled = workers > 1

        st.divider()
        
        def on_start_tests():
            """Callback when Start Tests is clicked"""
            # CRITICAL: Reset results immediately so sidebar shows 0s during new run
            st.session_state.test_runner.results = {'passed': 0, 'failed': 0, 'total': 0}
            st.session_state.output_lines = []
            
            results_dir, static_dir, base_dir = allure_paths()
            
            # Clean Allure directories with better error handling
            try:
                # Force remove results directory
                if os.path.exists(results_dir):
                    shutil.rmtree(results_dir, ignore_errors=False)
                    print(f"[Cleanup] Removed old results: {results_dir}", flush=True)
                
                # Recreate clean results directory
                os.makedirs(results_dir, exist_ok=True)
                print(f"[Cleanup] Created fresh results dir: {results_dir}", flush=True)
                
                # Clean static report directory
                if os.path.exists(static_dir):
                    shutil.rmtree(static_dir, ignore_errors=False)
                    print(f"[Cleanup] Removed old static report: {static_dir}", flush=True)
                    
            except Exception as e:
                print(f"⚠️ Error cleaning Allure dirs: {e}", flush=True)
                st.toast(f"⚠️ Warning: Could not clean old results: {e}", icon="⚠️")

            st.session_state.report_refresh_token = 0
            st.session_state.auto_generate_report = False
            st.session_state.active_tab = "🌐 Live Browser View"  # Switch to browser view when starting
            
            # Start Selenium nodes if in Docker
            if vnc_available:
                start_selenium_nodes(st.session_state.parallel_workers)
                time.sleep(3)

            tag_map = {
                "All Tests": None,
                "Smoke Tests (@smoke)": "@smoke",
                "Login Tests (@login)": "@login"
            }
            selected_tag = tag_map.get(st.session_state.test_suite, None)
            st.session_state.test_runner.run_tests(tags=selected_tag)
            st.session_state.tests_were_running = True
            st.session_state.last_update = time.time()
        
        def on_stop_tests():
            """Callback when Stop Tests is clicked"""
            st.toast("⏹️ Stopping tests...", icon="🛑")
            st.session_state.test_runner.stop_tests()
            if vnc_available:
                stop_selenium_nodes()
            st.session_state.tests_were_running = False
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("▶️ Start Tests",
                     disabled=test_runner.is_running,
                     use_container_width=True,
                     type="primary",
                     on_click=on_start_tests)
        with col2:
            st.button("⏹️ Stop Tests",
                     disabled=not test_runner.is_running,
                     use_container_width=True,
                     on_click=on_stop_tests)

        st.divider()
        if test_runner.is_running:
            msg = f"🔄 Tests running in parallel ({st.session_state.parallel_workers} workers)..." if parallel_enabled \
                  else "🔄 Tests running..."
            st.success(msg)
            
            # Show auto-refresh indicator
            elapsed = time.time() - st.session_state.last_update
            st.caption(f"🔄 Auto-updating... (Last: {datetime.now().strftime('%H:%M:%S')})")
        else:
            st.info("👉 Click 'Start Tests' to begin")

        st.subheader("📊 Test Results")
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.metric("✅ Passed", test_runner.results['passed'])
        with cm2:
            st.metric("❌ Failed", test_runner.results['failed'])
        with cm3:
            # Show "-" when tests are running and total is 0
            total_display = "-" if (test_runner.is_running and test_runner.results['total'] == 0) else test_runner.results['total']
            st.metric("📊 Total", total_display)

        def on_load_allure_results():
            """Load accurate results from Allure JSON files"""
            accurate_results = get_allure_test_counts()
            if accurate_results['total'] > 0:
                st.session_state.test_runner.results = accurate_results
                st.toast(f"✅ Loaded {accurate_results['total']} test results from Allure", icon="📊")
            else:
                st.toast("⚠️ No Allure results found", icon="⚠️")

        if st.button("📊 Load from Allure", use_container_width=True, disabled=test_runner.is_running, 
                     on_click=on_load_allure_results,
                     help="Read accurate test counts from Allure result files"):
            pass

        st.divider()
        st.subheader("🔗 Quick Links")
        if vnc_available:
            def vnc_link(port: int, label: str) -> str:
                # Same params we use in the iframe so the view is scaled and centered
                return f"http://localhost:{port}/?autoconnect=1&resize=scale&view_clip=false"

            st.markdown(f"- [🌐 VNC Node 1]({vnc_link(7900, 'VNC Node 1')})")
            if st.session_state.parallel_workers >= 2:
                st.markdown(f"- [🌐 VNC Node 2]({vnc_link(7910, 'VNC Node 2')})")
            if st.session_state.parallel_workers >= 3:
                st.markdown(f"- [🌐 VNC Node 3]({vnc_link(7920, 'VNC Node 3')})")
            if st.session_state.parallel_workers >= 4:
                st.markdown(f"- [🌐 VNC Node 4]({vnc_link(7930, 'VNC Node 4')})")  # 🔹 NEW
            if st.session_state.parallel_workers >= 5:
                st.markdown(f"- [🌐 VNC Node 5]({vnc_link(7940, 'VNC Node 5')})")  # 🔹 NEW

            st.markdown("- [🐳 Selenium Hub](http://localhost:4444)")
            st.success("✅ Selenium services running!")



    # Tabs with active tab tracking
    tabs = st.tabs(["🌐 Live Browser View", "📋 Console Output", "📊 Allure Report"])
    
    # Determine which tab to show (based on session state)
    tab_names = ["🌐 Live Browser View", "📋 Console Output", "📊 Allure Report"]
    active_idx = tab_names.index(st.session_state.active_tab) if st.session_state.active_tab in tab_names else 0

    # Tab 1: Live Browser
    with tabs[0]:
        if vnc_available:
            st.subheader("Live Browser Automation")

            parallel_enabled = bool(int(os.environ.get('PARALLEL_WORKERS', '1')) > 1)
            num_workers = int(os.environ.get('PARALLEL_WORKERS', '1'))

            if parallel_enabled and num_workers > 1:
                num_workers = min(num_workers, 5)  # 🔺 allow up to 5
                cols = st.columns(num_workers if num_workers >= 2 else 1)
                vnc_ports = [7900, 7910, 7920, 7930, 7940]  # 🔹 add 4 & 5

                for i in range(num_workers):
                    with cols[i]:
                        st.markdown(f"**Browser {i+1}**")
                        vnc_url = f"http://localhost:{vnc_ports[i]}/?autoconnect=1&resize=scale&view_clip=false"
                        st.markdown(
                            f"""
                            <div style="position:relative;width:100%;height:400px;">
                                <iframe 
                                    src="{vnc_url}" 
                                    style="position:absolute;top:0;left:0;width:100%;height:100%;
                                           border:2px solid #444;border-radius:8px;background-color:#000;">
                                </iframe>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.caption(f"[Open Node {i+1}](http://localhost:{vnc_ports[i]})")
                st.info(f"🚀 Tests running in parallel across {num_workers} browsers!")
            else:
                vnc_url = "http://localhost:7900/?autoconnect=1&resize=scale&view_clip=false"
                st.markdown(
                    f"""
                    <div style="position:relative;width:100%;height:85vh;">
                        <iframe 
                            src="{vnc_url}" 
                            style="position:absolute;top:0;left:0;width:100%;height:100%;
                                   border:2px solid #444;border-radius:8px;background-color:#000;">
                        </iframe>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption(f"🔗 Direct access: [Open in new tab]({vnc_url})")
        else:
            st.info(
                """
                **🐳 Docker Mode Not Active**

                To enable live browser streaming (optional):
                ```bash
                docker-compose -f docker-compose.demo.yml up --build
                ```
                Services:
                - Streamlit Demo: http://localhost:8501
                - Live Browser View: http://localhost:7900
                - Static Allure Server: http://localhost:8666
                """
            )

    # Tab 2: Console Output
    with tabs[1]:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader("Test Execution Output")
        with c2:
            if st.button("🔄 Refresh Output", key="refresh_console"):
                st.rerun()

        if st.session_state.output_lines:
            output_text = "\n".join(st.session_state.output_lines[-100:])
            st.text_area("Console Output", value=output_text, height=500, disabled=True, label_visibility="collapsed")
        else:
            st.info("Console output will appear here when tests start...")

    # Tab 3: Allure Report (Static)
    with tabs[2]:
        st.subheader("📊 Allure Test Report")

        results_dir, static_dir, base_dir = allure_paths()

        # Auto-generate report if flag is set
        if st.session_state.auto_generate_report:
            st.session_state.auto_generate_report = False  # Reset flag
            with st.spinner("Generating Allure report..."):
                ok, msg = allure_generate_static()
                if ok:
                    st.session_state.report_refresh_token += 1
                    
                    # Update sidebar results from Allure
                    accurate_results = get_allure_test_counts()
                    if accurate_results['total'] > 0:
                        st.session_state.test_runner.results = accurate_results
                    
                    st.success("✅ Allure report generated successfully!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to generate report: {msg}")

        colA, colB = st.columns(2)
        with colA:
            if st.button("🧱 Generate / Refresh Static Report", key="refresh_allure_static", use_container_width=True, disabled=test_runner.is_running):
                ok, msg = allure_generate_static()
                if ok:
                    st.session_state.report_refresh_token += 1
                    
                    # Update sidebar results from Allure
                    accurate_results = get_allure_test_counts()
                    if accurate_results['total'] > 0:
                        st.session_state.test_runner.results = accurate_results
                    
                    st.success(msg)
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(msg)
                    with st.expander("Show generator output / diagnostics"):
                        st.code(msg)

        with colB:
            if os.path.exists(static_dir) and os.listdir(static_dir):
                st.success("✅ Static report ready")
            else:
                st.info("No static report yet. Generate it after a test run.")

        # Display report
        if os.path.exists(static_dir) and os.listdir(static_dir):
            # Try to start the server
            start_static_server_once(base_dir, preferred_port=8666)

            # Check server health
            server_ok = False
            port = None
            
            if 'static_server' in st.session_state:
                meta = st.session_state.static_server
                port = meta.get('port')
                server_running = meta.get('running', False)
                
                if server_running and port:
                    try:
                        with socket.create_connection(("127.0.0.1", port), timeout=1):
                            server_ok = True
                    except Exception:
                        pass

            # Try to show the iframe
            if server_ok and port:
                bust = f"{int(time.time())}_{st.session_state.report_refresh_token}"
                iframe_url = f"http://localhost:{port}/allure-static/index.html?cb={bust}"
                
                st.markdown(
                    f"""
                    <iframe src="{iframe_url}" width="100%" height="700"
                            style="border:2px solid #444;border-radius:8px;"></iframe>
                    """,
                    unsafe_allow_html=True
                )
                st.caption(f"🔗 [Open in new tab]({iframe_url})")
            else:
                st.error("❌ Could not start static file server")
                
                # Alternative: Show file paths for manual access
                idx = os.path.join(static_dir, "index.html")
                st.info(f"**Report location:** `{idx}`")
        else:
            st.info(
                """
                **No test results yet**

                1. Click **Start Tests** to run your test suite
                2. Report will be generated automatically when tests complete
                3. Or click **Generate / Refresh Static Report** manually
                """
            )

    # Auto-refresh trigger (only when tests are running)
    # This uses Streamlit's built-in rerun with a delay
    if test_runner.is_running and not tests_completed:
        time.sleep(2)
        st.rerun()
    
    # If tests just completed and we switched tabs, rerun to show the report
    if tests_completed:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()
