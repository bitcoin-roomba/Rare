# Contributing

## What you can do

### Add translations

1. Execute ```pylupdate5 $(find -name "*.py") -ts Rare/languages/de.ts``` in source directory. Replace *de* with your
   language code
2. Modify the .ts file manually or in Qt Linguist
3. Compile the file with ```lrelease Rare/languages/{lang}.ts```

If compilation fails, just push ts file. Then I will compile it

### Add Stylesheets

For this you can create a .qss file in Rare/Styles/ directory or modify the existing RareStyle.qss file. Here are some
examples:
[Qt Docs](https://doc.qt.io/qt-5/stylesheet-examples.html)

### Add features

Select one Card of the project and implement it, or if you want to add another feature ask me on Discord, or create an
issue on GitHub

## Git crash-course

To contribute fork the repository and clone **your** repo. Then make your changes, add it to git with `git add File.xy`
and upload it to GitHub with `git commit -m "message"` and `git push`. Some IDEs can do this automatically.

If you uploaded your changes, create a pull request
