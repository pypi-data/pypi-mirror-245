A Python library that streamlines your repository creation and commits on Github in 2 lines of code. 

#### Features
1. Repository creation
2. Commits to existing repository
3. Automatically Merge conflicts resolved 
4. High-level wrapper

I've built this library to both explore how Github API works and ease my process to create and commit to my Github account. If you're using VS Code editor, it should already be streamlined but for beginners it is not that straightforward. Besides, resolving merge conflicts is another pain that one-might encounter while doing push through git interface (bash). That is why, I have developed this project. 

#### Long-term plan

Developing a total terminal interface through which users can perform almost any operation on Github. 

### Prerequisites

1. GitHub account
2. Github Personal Access Token (Fine-grained version)
3. Python 3.8. X installed


### Quickstart
Installing
```bash
pip install pushbot
```
importing the library
```python
from pushbot import push_repo
push_repo()
```