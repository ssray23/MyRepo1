package com.suddha;

public class Shape {

    private String shapeName = "";

    public void setShape(String iShape){
        this.shapeName = iShape;
    }
    public void printShape(){
        System.out.println("I am a " + this.shapeName);
    }

}
