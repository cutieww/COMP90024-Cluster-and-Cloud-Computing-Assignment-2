'''
  Team 84 - Melbourne
  Brendan Pichler(bpichler@student.unimelb.edu.au) 1212335
  George Wang (wagw@student.unimelb.edu.au) 1084224
  Luchen Zhou(luczhou@student.unimelb.edu.au) 1053412
  Wei Wang(wangw16@student.unimelb.edu.au) 900889
  Yihan Wang (yihwang3@student.unimelb.edu.au) 1056614
'''
import subprocess
import sys

def main():
    #fastapi_server = subprocess.Popen(["uvicorn", "fastapi_server:app", "--reload"])
    fastapi_server = subprocess.Popen(["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    mastodon_stream = subprocess.Popen([sys.executable, "mastodon_process.py"])

    try:
        fastapi_server.wait()
        mastodon_stream.wait()
    except KeyboardInterrupt:
        fastapi_server.terminate()
        mastodon_stream.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()