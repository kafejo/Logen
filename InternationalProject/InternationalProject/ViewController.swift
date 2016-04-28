//
//  ViewController.swift
//  InternationalProject
//
//  Created by Aleš Kocur on 27/04/16.
//  Copyright © 2016 Aleš Kocur. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        title = NSLocalizedString("viewcontroller.navigation_title", comment: "Navigation bar title of my ViewController")
        title = NSLocalizedString("viewcontroller.navigation_title2", comment: "")
        title = NSLocalizedString("viewcontroller.navigation_title3", bundle: NSBundle.mainBundle(), comment: "Navigation bar title")
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

