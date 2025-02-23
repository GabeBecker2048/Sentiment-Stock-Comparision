from lib.settings import Settings
import subprocess
from sys import argv, executable

def run_subprocess(command: list, outstream=None):
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Output: {result.stdout}\n", file=outstream)
    print(f"Errors: {result.stderr}\n", file=outstream)
    return result

def main():
    largv = [str(arg).lower() for arg in argv]
    settings_filename = './lib/settings.json'
    for i in range(len(largv)):
        if largv[i][:10] == '-settings=':
            settings_filename = argv[i][10:]

    CLI_Settings = Settings(settings_filename)
    for i, (arg, larg) in enumerate(zip(largv, argv)):
        if '--settingsmod' == larg:
            if not CLI_Settings.settingsmod(argv[i+1]):
                print("Invalid settingsmod argument given. The settings will not be changed")
            else:
                print(f"The settings at '{settings_filename}' have been adjusted! {argv[i+1]}")
        elif '--run' == larg:
            run_subprocess([executable, "./lib/generate_articles.py"])
            run_subprocess([executable, "./lib/generate_stock_report.py"])
            run_subprocess([executable, "./lib/sentiment_analysis.py"])
            run_subprocess([executable, "./lib/graph_sentiment.py"])
            run_subprocess([executable, "./lib/graph_correlation.py"])
        elif '--news' == larg:
            run_subprocess([executable, "./lib/generate_articles.py"])
        elif '--stock' == larg:
            run_subprocess([executable, "./lib/generate_stock_report.py"])
        elif '--sentiment' == larg:
            run_subprocess([executable, "./lib/sentiment_analysis.py"])
        elif '--graph' == larg:
            run_subprocess([executable, "./lib/graph_sentiment.py"])
            run_subprocess([executable, "./lib/graph_correlation.py"])

if __name__ == "__main__":
    main()
