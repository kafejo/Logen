# Logen - Localization generator
Tool for lightweight continuous internationalization of Swift or Objective-C projects. 

## Use case
You find yourself in a stage of project when there are localizations and you typically have spreadsheet with localizations or you want to translate them by yourself. You added new controller and there are new NSLocalizationString() functions (or macros in obj-c case) and you want them to translate so you have to scan your newly added code and add keys you found in all versions of your Localizable.strings file.

**TLDR; Logen scans your code for NSLocalizationString keys and comments and appends new (or rewrites current) to your Localizable.strings**

## Usage

    python3 Logen.py -i <inputdirectory> -o <outputfile> -r -v 

## Options
**-r** rewrites the output file (not append)

**-i** input directory, subdirectories will be scanned too, '.' if not given

**-o** output file, Localizable.strings if not given

**-v** or **--verbose** enables verbose mode


## Example

Lets say there is localization file Localizable.strings with content

```swift
/* Navigation bar title of login controller */
"login.navigation_title" = "";

/* Navigation bar title of my ViewController */
"viewcontroller.navigation_title" = "";
```

And we add new keys into our ViewController:

```swift
title = NSLocalizedString("viewcontroller.navigation_title2", comment: "")
title = NSLocalizedString("viewcontroller.navigation_title3", bundle: NSBundle.mainBundle(), comment: "Navigation bar title")
```

We run Logen in order to update our Localizable.strings file

    python3 Logen.py -i InternationalProject/InternationalProject 

Logen will update all language's Localizable.strings by appending missing keys.

Result

```swift
/* Navigation bar title of login controller */
"login.navigation_title" = "";

/* Navigation bar title of my ViewController */
"viewcontroller.navigation_title" = "";

/* No comment provided */
"viewcontroller.navigation_title2" = "";

/* Navigation bar title */
"viewcontroller.navigation_title3" = "";
```

## TODO
- ~Scan for multiple languages at once~
- Updating comments of current keys
- Multiple tables support
- Create PyPI package for easy installation

## Author
Aleš Kocur, ales@thefuntasty.com

## Licence
Logen is available under the MIT license. See the LICENSE file for more info.
