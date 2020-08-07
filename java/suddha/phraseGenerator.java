package suddha;

public class phraseGenerator {

	public static void main (String[] args) {
	
		String[] wordListOne = {"I", "We", "Suddha", "They", "You", "Jim", "Sai", "Frankie", "Chandan", "Dan", "David"};
		String[] wordListTwo = {"beg", "bark", "eat", "eats bacon", "drink", "drink cheap beer", "say", "rant", "moan", "laugh", "cry"};
		String[] wordListThree = {"all the time", "in front of Reg's office", "in the classroom", "at home", "at school", "at work", "in front of the reception", "in the forest", "in the toilet"};
		
		int oneLength = wordListOne.length;
		int twoLength = wordListTwo.length;
		int threeLength = wordListThree.length;
		
		int rand1 = (int) (Math.random() * oneLength);
		int rand2 = (int) (Math.random() * twoLength);
		int rand3 = (int) (Math.random() * threeLength);
		
		String phrase = wordListOne[rand1] + " " + wordListTwo[rand2] + " " + wordListThree[rand3] + ".";
		
		System.out.println("The Phrase : " + phrase);
		
	} //end of main()
	
} // end of class