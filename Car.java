package com.suddha;

public class Car {

    private String CarName;
    private int CarYear ;

    // Default Quick Constructor
    public  Car () {
        this.CarName = "";
        this.CarYear = 0;
    };

    // Constructor takes inputs
    public  Car (String iName, int iYear) {
        this.CarName = iName;
        this.CarYear = iYear;
    };
    //Print Car Method
    public void PrintCar() {
        System.out.println("Car Print : " + this.CarName + " .. of year " + this.CarYear);
    };

    // Method to change a car
    public void WriteCar(String iName, int iYear) {
        this.CarName = iName;
        this.CarYear = iYear;
    };

}
