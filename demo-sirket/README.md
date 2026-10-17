\# Company Simulation (Demo)



\*\*All data in this folder is fake.\*\* It simulates a fictional logistics company whose app leaks secrets in its error output.



1\. Run it directly: `python demo-sirket/app.py` → the error exposes the DB password, API key, server IP, support email and your Windows username.

2\. Run it through TermiMind → all of these are replaced with `\*\*\*`, while the error type, port and line number stay readable so the model can still explain the problem.



The file is named `sirket.env` instead of `.env` on purpose, so it is not ignored by `.gitignore`.

