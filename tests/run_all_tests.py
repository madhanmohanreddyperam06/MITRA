"""Run all tests for MITRA using pytest.

This script provides a convenient way to run all tests with pytest,
supporting different test categories and configurations.

Usage:
    python tests/run_all_tests.py              # Run all tests
    python tests/run_all_tests.py --unit       # Run only unit tests
    python tests/run_all_tests.py --integration # Run only integration tests
    python tests/run_all_tests.py --mysql      # Run MySQL-specific tests
    python tests/run_all_tests.py --cov        # Run with coverage
"""
import sys
import os
import subprocess
import argparse


def run_pytest(args):
    """Run pytest with specified arguments."""
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Build pytest command
    cmd = [sys.executable, "-m", "pytest", "tests/"]

    # Add pytest arguments
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.mysql:
        cmd.extend(["-m", "mysql"])

    # Add coverage if requested
    if args.coverage:
        cmd.extend([
            "--cov=backend/app",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])

    # Add verbose output
    cmd.append("-v")

    # Run pytest
    print(f"\n{'='*60}")
    print("Running pytest with command:")
    print(" ".join(cmd))
    print('='*60 + "\n")

    result = subprocess.run(cmd, cwd=project_root)
    return result.returncode


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run MITRA tests using pytest"
    )
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--mysql",
        action="store_true",
        help="Run only MySQL-specific tests (requires MySQL database)"
    )
    parser.add_argument(
        "--cov",
        action="store_true",
        help="Run tests with coverage report"
    )

    args = parser.parse_args()

    # If no specific category is selected, run all tests except MySQL
    if not (args.unit or args.integration or args.mysql):
        print("Running all tests (unit + integration)")
        print("Use --mysql to run MySQL-specific tests\n")

    return run_pytest(args)


if __name__ == "__main__":
    sys.exit(main())
