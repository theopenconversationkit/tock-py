
.PHONY: help clean-build build-check bump-snapshot bump-release-major bump-release-minor bump-release-patch install lint

help: ## Display this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'


clean-build: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

build-check: clean-build ## Build and check the distribution
	python -m build
	twine check dist/*

bump-snapshot: clean-build ## Bump version and build snapshot
	bumpversion build;
	python -m build;
	twine upload dist/*

bump-release-major: clean-build ## Bump major version and build release
	bumpversion major;
	python -m build;
	twine upload dist/*

bump-release-minor: clean-build ## Bump minor version and build release
	bumpversion minor;
	python -m build;
	twine upload dist/*

bump-release-patch: clean-build ## Bump patch version and build release
	bumpversion patch;
	python -m build;
	twine upload dist/*

install: ## Install the package and its dependencies
	pip install -r requirements.txt

lint: ## Lint the code using flake8
	flake8 ./tock