import com.suddha.*;

public class OddNumbers {
	
	public static void main(String args[]) {
		
		int n = 100;
		
		System.out.print("Odd Numbers from 1 to " + n + " are: ");
		
		for (int i = 1; i <= n; i++) {
			if (i%2 != 0) {
				System.out.print(i + " ");
				
			}
		}

		// Line separator
		System.out.println();

		// Creating a car just for fun  ;-)
		// Create a car object using default constructor
		Car myGreatCar  = new Car();

		// Default constructor does not set attributes of myGreatCar Car
		myGreatCar.PrintCar();

		// Set the attributes for myGreatCar using the WriteCar method and then print it using PrintCar method
		myGreatCar.WriteCar("Vauxhall", 2008);
		myGreatCar.PrintCar();
	}
}
