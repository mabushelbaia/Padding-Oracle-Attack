n ?= 5
.PHONY: run	bytes 
run:
	@echo "[5 Bytes] 12345"
	@echo -n "12345" | openssl enc -aes-128-cbc -e -k hi -md sha256 -pbkdf2 | openssl enc -aes-128-cbc -d -nopad -k hi -md sha256 -pbkdf2 | xxd

	@echo "\n[10 Bytes] 0123456789"
	@echo -n "0123456789" | openssl enc -aes-128-cbc -e -k hi -md sha256 -pbkdf2 | openssl enc -aes-128-cbc -d -nopad -k hi -md sha256 -pbkdf2 | xxd
	
	@echo "\n[16 Bytes] 0123456789ABCDEF"
	@echo -n "0123456789ABCDEF" | openssl enc -aes-128-cbc -e -k hi -md sha256 -pbkdf2 | openssl enc -aes-128-cbc -d -nopad -k hi -md sha256 -pbkdf2 | xxd
bytes:
	@echo "[${n} Bytes]"
	@printf '%*s' "${n}" | tr ' ' 'X'| openssl enc -aes-128-cbc -e -k hi -md sha256 -pbkdf2 | openssl enc -aes-128-cbc -d -nopad -k hi -md sha256 -pbkdf2 | xxd

attack:
	python3 manual_attack.py
help:
	@echo "\033[34mmake\033[0m: default run with 5, 10, 16 bytes."
	@echo "\033[34mmake bytes n=i\033[0m: where i is the number of bytes."