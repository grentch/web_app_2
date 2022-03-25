
import sys
from streamlit import cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "page.py"]
    sys.exit(stcli.main())

#use python open_app.py to run the project