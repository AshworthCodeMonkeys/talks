# Using Git for version control

## Useful links

[Obligatory xkcd comic](http://www.xkcd.com/1597/)

[Comic explanation](http://explainxkcd.com/wiki/index.php/1597:_Git)

[Git Documentation](https://git-scm.com/doc)

[Git cheat sheet](https://training.github.com/kit/downloads/github-git-cheat-sheet.pdf)

[Github](https://github.com)

[Bitbucket](https://bitbucket.org)

[Gitflow](http://nvie.com/posts/a-successful-git-branching-model/)

[Stack Overflow - top questions](http://stackoverflow.com/questions?sort=votes)

[Patronising google link](http://google.co.uk/search?q=git)

[how git works](http://maryrosecook.com/blog/post/git-from-the-inside-out)

[javascript implementation](http://gitlet.maryrosecook.com/)

## Specific links

[add vs. commit -a](https://lostechies.com/jasonmeridth/2009/09/10/quot-git-commit-a-quot-and-quot-git-add-quot/)

pull vs. fetch [Stack Overflow](http://stackoverflow.com/questions/292357/what-are-the-differences-between-git-pull-and-git-fetch) and [git-scm](https://git-scm.com/docs/git-fetch)

branch vs. tag [Stack Overflow](http://stackoverflow.com/questions/1457103/how-is-a-tag-different-from-a-branch-which-should-i-use-here) and [git-scm](https://git-scm.com/book/en/v2/Git-Basics-Tagging)

## Three states
####(How the important bit got confused)

From the documentation:
>Now, pay attention. This is the main thing to remember about Git if you want the rest of your learning process to go smoothly. Git has three main states that your files can reside in: committed, modified, and staged. Committed means that the data is safely stored in your local database. Modified means that you have changed the file but have not committed it to your database yet. Staged means that you have marked a modified file in its current version to go into your next commit snapshot.

From this, the git repository has three main sections: working directory, staging area and .git directory (repository)

> The Git directory is where Git stores the metadata and object database for your project. This is the most important part of Git, and it is what is copied when you clone a repository from another computer.

So my explanation became confused when I took the idea of three states/stages but then considered that modified files in the working directory may be tracked or untracked - only tracked (`git add`ed) files can be staged.

Things got worse when I tried to rescue the idea of three stages by adding a fifth as working with a remote repository add a `git push` at the end.

So hopefully that's at least begun to unravel the important states/stages/sections the rest of your learning process can indeed now go smoothly...

## Why use version control?

    analysis
    ├── infiles
    │   ├── data.txt
    │   ├── data.new.txt
    │   ├── data.forpaper.txt
    │   └── data.final.txt
    └── outfiles
        ├── result.txt
        ├── result2.txt
        ├── result.final.txt
        ├── result.finalfinal.txt
        └── result.finalfinal2.txt

## Why use Git?
### Distributed version control system
* Local version control (hard to share)
* Centralised version control (depends on network connection)
* Distributed version control (just right)

### File/directory snapshots

    analysis
    ├── .git
    ├── infiles
    │   └── data.txt
    └── outfiles
        └── result.txt


### Checksums

    analysis
    ├── .git
    ├── 3ca2e596565a6b7a662794ea02b242fddc27da14
    │   └── 5332132ce3440a7d7a98505f0522c069c302f6ef
    └── 8b0d246b473975a61a168481d5119c682f0974fc
        └── bf770c934917c86c1eb43ef02f3d0893ebe141a1


### Most operations add data

Only undo operations can't be undone

## Getting started
Install command line tools/GUI

### Basic setup

    $ git config --global user.name "Richard Challis"
    $ git config --global user.email rjchallis@gmail.com

### First repository

    $ mkdir test
    
    $ cd test
    
    $ git init
    Initialized empty Git repository in /Users/rchallis/projects/test/.git/
    
    $ echo "Hello" > README
    
    $ git add README
    
    $ git commit -m "my first commit"
    [master (root-commit) 5393713] my first commit
     1 file changed, 1 insertion(+)
     create mode 100644 README

	$ echo "Code Monkeys" >> README
    
    $ git commit -a -m 'second commit'
    [develop 540a723] second commit
     1 file changed, 1 insertion(+)
    
    $ git log
    commit 540a723b74870c29bbe70ae06353dc6c1d4f137d
    Author: Richard Challis <rjchallis@gmail.com>
    Date:   Thu Jan 14 10:09:38 2016 +0000
    
        second commit
    
    commit 5393713f42fc45de6eeac6b3e742ada6d46aab6e
    Author: Richard Challis <rjchallis@gmail.com>
    Date:   Thu Jan 14 10:07:10 2016 +0000
    
        my first commit


### Changing a commit message

    $ git commit --amend -m "mention Code Monkeys"
    [develop 3889612] mention Code Monkeys
     Date: Thu Jan 14 10:09:38 2016 +0000
     1 file changed, 1 insertion(+)

    $ git log
    commit 38896126deea7406f04fd0f6f70023cee832a427
    Author: Richard Challis <rjchallis@gmail.com>
    Date:   Thu Jan 14 10:09:38 2016 +0000

        mention Code Monkeys

    commit 5393713f42fc45de6eeac6b3e742ada6d46aab6e
    Author: Richard Challis <rjchallis@gmail.com>
    Date:   Thu Jan 14 10:07:10 2016 +0000

        my first commit


## Branches

    $ git status
    On branch master
    nothing to commit, working directory clean
    
    $ #git branch develop
    $ git checkout -b develop
    $ git status
    On branch develop
    nothing to commit, working directory clean
    
    $ echo '(and rest of world)' >> README
    $ git commit -a -m 'greet rest of world'
    $ cat README
    hello
    Code Monkeys
    (and rest of world)
    
    $ git checkout master
    $ cat README
    hello
    Code Monkeys
    
    $ git merge develop
    $ git status
    On branch master
    nothing to commit, working directory clean
    
    $ cat README
    hello
    Code Monkeys
    (and rest of world)
    
	$ git checkout develop
	

## Remotes

    $ git remote add origin https://github.com/rjchallis/test.git
    
    $ git push -u origin master
    Counting objects: 6, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (6/6), 462 bytes | 0 bytes/s, done.
    Total 6 (delta 0), reused 0 (delta 0)
    To https://github.com/rjchallis/test.git
     * [new branch]      master -> master
    Branch master set up to track remote branch master from origin.
    
    $ git pull
	Already up-to-date.
    
    $ cd ../
    
    $ git clone https://github.com/rjchallis/test.git clone
    Cloning into 'clone'...
    remote: Counting objects: 6, done.
    remote: Compressing objects: 100% (2/2), done.
    remote: Total 6 (delta 0), reused 6 (delta 0), pack-reused 0
    Unpacking objects: 100% (6/6), done.
    Checking connectivity... done.

    $ cd clone
    
    $ sed -i '' 's/od/lon/' README 
    
    $ git checkout -b develop
    M	README
    Switched to a new branch 'develop'

    $ git commit -a -m 'change greeting'
    [develop 1fa583a] change greeting
     1 file changed, 1 insertion(+), 1 deletion(-)

    $ git checkout master
    Switched to branch 'master'
    Your branch is up-to-date with 'origin/master'.
    
    $ git merge develop
    Updating 3889612..1fa583a
    Fast-forward
     README | 2 +-
     1 file changed, 1 insertion(+), 1 deletion(-)
    
    $ git push
    Counting objects: 3, done.
    Writing objects: 100% (3/3), 267 bytes | 0 bytes/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    To https://github.com/rjchallis/test.git
       3889612..1fa583a  master -> master
       
    $ cd ../test
    
    $ git status
    On branch master
    Your branch is up-to-date with 'origin/master'.
    nothing to commit, working directory clean

    $ git fetch
    remote: Counting objects: 3, done.
    remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
    Unpacking objects: 100% (3/3), done.
    From https://github.com/rjchallis/test
       3889612..1fa583a  master     -> origin/master

    $ git status
    On branch master
    Your branch is behind 'origin/master' by 1 commit, and can be fast-forwarded.
      (use "git pull" to update your local branch)
    nothing to commit, working directory clean
    
    $ #git pull
    
## Conflicts

    $ sed -i '' 's/M/D/' README 
    
    $ cat README
    Hello
    Code Donkeys
    
    $ git commit -a -m 'change taxon'
    [master d846981] change taxon
     1 file changed, 1 insertion(+), 1 deletion(-)
    
    $ git status
    On branch master
    Your branch and 'origin/master' have diverged,
    and have 1 and 1 different commit each, respectively.
      (use "git pull" to merge the remote branch into yours)
    nothing to commit, working directory clean
    
    $ git pull
    Auto-merging README
    CONFLICT (content): Merge conflict in README
    Automatic merge failed; fix conflicts and then commit the result.
    
    $ cat README
    hello
    <<<<<<< HEAD
    Code Donkeys
    =======
    Clone Monkeys
    >>>>>>> 1fa583a9c653fa20fecb9c74d252228db1bc560c
    
    $ nano README
    
    $ git commit -a -m 'resolve merge conflict'
    [master 4b63679] resolve merge conflict
    
    $ git push
    Counting objects: 6, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (6/6), 533 bytes | 0 bytes/s, done.
    Total 6 (delta 0), reused 0 (delta 0)
    To https://github.com/rjchallis/test.git
       1fa583a..4b63679  master -> master

## Using branches to manage features and releases
[Gitflow](http://nvie.com/posts/a-successful-git-branching-model/)

