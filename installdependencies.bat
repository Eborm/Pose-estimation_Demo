(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe', 'C:\Tools\python-3.12.5.exe')

C:\Tools\python-3.12.5.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

pip install --upgrade pip
pip install opencv-python mediapipe
