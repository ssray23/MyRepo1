"suddha" is the user-created package and contains all Java classes created by Suddha Satta Ray
package name must be same as the folder name where these individual class files are housed.

To compile classes inside the suddha folder, come up one level where you can see the folder suddha
In my setup, the "suddha" folder is just under the folder called "java" i.e. C:\Box Sync\Essentials\Files\MyRepo1\java\suddha
So, I change to this "java" folder and then start compiling my classes as below using the javac command:

Compile: 
-----------
C:\Box Sync\Essentials\Files\MyRepo1\java> javac   .\suddha\myFirstApp.java
C:\Box Sync\Essentials\Files\MyRepo1\java> javac   .\suddha\Car.java

Run:
--------
To run a class file, we have to use the dot notation and prefix the class with its package. 
Once you start using packages in Java Language, the class name gets "linked" with the package it belongs to:

C:\Box Sync\Essentials\Files\MyRepo1\java> java suddha.myFirstApp

Hey Suddha ..
How is it going? ..
Car Print : Toyota .. of year 2007