import sys
from lib.thread_analyzer import ThreadAnalyzer
from lib.report_printer import ReportPrinter

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python thread_summary.py <thread_id>")

    thread_id = sys.argv[1]

    try:
        analyzer = ThreadAnalyzer(thread_id)
        printer = ReportPrinter(analyzer)

        analyzer.analyze_thread()
        printer.print_thread_analysis(thread_id)
    except Exception:
        sys.exit("Thread not found")
