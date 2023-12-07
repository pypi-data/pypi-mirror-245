from setuptools import setup
def readme():
    return (
'''
# TestMyFirstProjectLibrary #

This is a super puper project that will help you do the exam
## How to use ##

To use it you should write:

```import MyFirstProjectLibrary as HelpTo```
1. ```HelpTo.Find.``` _YourCommand_

or
2. ```HelpTo.Documentation.``` `Something`

## Commands ##

1. `Documentation.Creator()` - print Creator
2. `Documentation.Commands()` - print all functions

---

1. `LongestHoatic_str(file, string)` - finds the longest sequence of this string in the file (Hoatic string!!!)
2. `Find.TheMostUsed_char(string)` - Find The Most Used char =)
3. `Find.Longest_char(file, char)` - finds the longest sequence of this character in the file

![](http://yt3.googleusercontent.com/BkY_WQddaB4GsucAVsdicLcGR5G5I-j2n-lQa8yL74ShjNSzdxlILmF68VlhXbPFd0BsdrM3Dg0=s100-c-k-c0x00ffffff-no-rj)

''')

setup(name='TestMyFirstProjectLibrary',
      long_description=readme(),
      long_description_content_type='text/markdown',
      version='0.0.7.0',
      description='None',
      packages=['TestMyFirstProjectLibrary'],
      author_email='akim.petbu@gmail.com')
