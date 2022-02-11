# Installing python

Following https://chamikakasun.medium.com/how-to-manage-multiple-python-versions-in-macos-2021-guide-f86ef81095a6  
`brew install openssl readline sqlite3 xz zlib`

`curl https://pyenv.run | bash` 

```
➜  ~ export PATH="/Users/markusnotti/.pyenv/bin:$PATH"
➜  ~ eval "$(pyenv init -)"
➜  ~ eval "$(pyenv virtualenv-init -)"
``` 

^Also add these to your ~/.zshrc

Use pyenv to install python: 
`➜  ~ pyenv install 3.10.2` 

Following https://packaging.python.org/en/latest/tutorials/managing-dependencies/ to manage dependencies w/ pipenv


Installing packages
`➜  wordle_solver pipenv install requests`

Running 
`➜  wordle_solver pipenv run python wordle_solver.py`


