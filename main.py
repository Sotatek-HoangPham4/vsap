import subprocess

def run(cmd):

    print(f"\nRunning: {cmd}")

    subprocess.run(
        cmd,
        shell=True,
        check=True
    )

def main():

    run(
        "python src/run_preprocessing.py"
    )

    run(
        "python src/run_analytics.py"
    )

if __name__ == "__main__":
    main()