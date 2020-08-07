package suddha;
import suddha.Car;

public class myFirstApp {
    
	public static void main(String[] args){

		// Print something
		System.out.println("Hey Suddha ..");
		System.out.println("How is it going? ..");

		// Reference one of your own executable class (i.e. TestCar)
		Car myCar = new Car("Toyota", 2007);
		myCar.PrintCar();

		
	}
}