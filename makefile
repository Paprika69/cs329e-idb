FILES :=                              \
    models.html                      \
    IDB2.log                       \
    test.py                        \
    models.py                    \
    unitest.py 						\
    .gitignore                    \
    requirements.txt                     \
    README.md                   \

#    collatz-tests/EID-RunCollatz.in   \
#    collatz-tests/EID-RunCollatz.out  \
#    collatz-tests/EID-TestCollatz.out \
#    collatz-tests/EID-TestCollatz.py  \

ifeq ($(shell uname), Darwin)          # Apple
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
else ifeq ($(CI), true)                # Travis CI
    PYTHON   := python3.5
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else ifeq ($(shell uname -p), unknown) # Docker
    PYTHON   := python                # on my machine it's python
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := python -m pydoc        # on my machine it's pydoc 
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python3.5
    PIP      := pip3
    PYLINT   := pylint3
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.5
    AUTOPEP8 := autopep8
endif


# collatz-tests:
# 	git clone https://github.com/cs329e-fall-2017/collatz-tests.git

.pylintrc:
	$(PYLINT) --disable=locally-disabled --reports=no --generate-rcfile > $@

models.html: models.py
	$(PYDOC) -w models

IDB2.log:
	git log > IDB2.log

# RunCollatz.tmp: RunCollatz.in RunCollatz.out RunCollatz.py
# 	$(PYTHON) RunCollatz.py < RunCollatz.in > RunCollatz.tmp
# 	diff RunCollatz.tmp RunCollatz.out

# TestCollatz.tmp: TestCollatz.py
# 	$(COVERAGE) run    --branch TestCollatz.py >  TestCollatz.tmp 2>&1
# 	$(COVERAGE) report -m                      >> TestCollatz.tmp
# 	cat TestCollatz.tmp

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -rf __pycache__

config:
	git config -l

format:
	$(AUTOPEP8) -i test.py
	$(AUTOPEP8) -i models.py
	$(AUTOPEP8) -i unitest.py

scrub:
	make clean
	rm -f  models.html
	rm -f  IDB2.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

runtests:
	$(PYTHON) unitest.py

reunserver:
	$(PYTHON) test.py

reqs:
	pip install -r requirements.txt

test: models.html IDB2.log check runtests
