# Logen - Localization generator

## Usage

    python Logen.py -a -i <inputdirectory> -o <outputfile>

## Options
**-a** append to the end of the output file

**-i** input directory, subdirectories will be scanned too, '.' if not given

**-o** output file, default.strings if not given

**-u** unsafe mode, it won't create backup file 

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

    python3 Logen.py -a -i InternationalProject/InternationalProject -o InternationalProject/InternationalProject/Base.lproj/Localizable.strings

Logen will update the Base language's Localizable.strings by appending missing keys.

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