# Padding Oracle Attack

🔗 | [Lab Description](docs/LAB.pdf) <br>
🔗 | [Lab Report](/docs/Padding_Oracle_Attack.pdf)

## Project Structure

```bash
./
├── docs/
│  ├── LaTeX/
│  │  ├── assets/
│  │  │  ├── d_diagram.png
│  │  │  ├── task1.png
│  │  │  ├── task2.png
│  │  │  ├── task3.1.png
│  │  │  ├── task3.2.png
│  │  │  └── task3.3.png
│  │  ├── cite.bib
│  │  ├── ieee.cls
│  │  ├── lix.sty
│  │  └── main.tex
│  ├── LAB.pdf*
│  └── Padding_Oracle_Attack.pdf*
├── src/
│  ├── docker-compose.yml
│  ├── Makefile
│  └── manual_attack.py*
└── README.md
```

## Installation and Running

clone the project using the following command:

```bash
git clone https://github.com/mabushelbaia/Padding-Oracle-Attack.git
cd Padding-Oracle-Attack
```
### Task 1:
```bash
make: default run with 5, 10, 16 bytes.
make bytes n=i: where i is the number of bytes.
```
### Task 2:
Skip this part its useless

### Task 3:
build and run the docker container make sure you have docker-compose installed `sudo apt install docker-compose`
```bash
docker-compose build
docker-compise up -d  #d for detched
```
Then you can run the script to decrypt the secret message.
```bash
python3 manual_attack.py
```

