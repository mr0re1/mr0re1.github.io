At their core, golden tests compare the current output of your code against a pre-saved "golden" output. If the current output matches the golden output, the test passes. If they differ, the test fails, signaling a potential issue.

To illustrate the usefulness of golden tests, let's take the example of [bla](https://github.com/mr0re1/bla) - a small Python library for performing code analysis.
Its repository has a folder [examples](https://github.com/mr0re1/bla/tree/main/examples) containing sample scripts showcasing its functionality.

One way to ensure that example scripts are not broken by code changes is to run them manually, the better way would be to automate it by adding "golden tests".

For golden tests to run, we need two things: something producing output and a reference output to compare it with.
The tested output is produced by invoking `python examples/<example>.py`.
The corresponding reference is stored in `tests/golden/expectations/<example>.out`.

See folder structure bellow:

```sh
.
├── .pre-commit-config.yaml
├── examples
│   ├── dekker.py
│   ├── halting.py
│   └── ...
├── tests
│   ├── golden
│   │   ├── expectations
│   │   │   ├── dekker.out
│   │   │   ├── halting.out
│   │   │   └── ...
│   │   └── run_tests.py
... # rest of the repo
```

The testing is done by [tests/golden/run_tests.py](https://github.com/mr0re1/bla/blob/main/tests/golden/run_tests.py). It's fairly simple:
* Iterates over all examples;
* Executes them and grabs the output;
* Compares the output with the reference and reports a failure if a mismatch is found;

  * [Optionally] updates the reference output.


**Why automatically update reference outputs?** <br> 

If the code change intentionally affects the output, manually updating multiple reference outputs can be tedious. That's why I've added the `--update` flag to the golden test runner.
<br>There is a risk of updating the reference output to an undesired one by accident, but if your workflow includes a review of the changes before merging (e.g., PR reviews), this risk is mitigated.


To **automatically execute** golden tests before committing, I've added them as a [pre-commit](https://pre-commit.com/) hook:

```yaml
# .pre-commit-config.yaml
repos:
-   repo: local
    hooks:
    - id: golden
      name: golden
      entry: python tests/golden/run_tests.py --update
      language: system
      types: [python]
      pass_filenames: false
```

Here is an example of how it looks:

```sh
$ git commit -a -m "Add halting example; minor output refactoring"
Check Yaml...........................................(no files to check)Skipped
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
black....................................................................Passed
golden...................................................................Failed
- hook id: golden
- exit code: 1
- files were modified by this hook

Running golden tests:
halting - FAIL: tests/golden/expectations/halting.out not found ... updating
inconsistency - PASS
dekker - FAIL: mismatch ... updated
 
# pre-commit failed due to golden test failure
# I've had to review changes in reference output, and
$ git add tests/golden/expectations/halting.out
$ git commit -a -m "Add halting example; minor output refactoring"
# OK
```



