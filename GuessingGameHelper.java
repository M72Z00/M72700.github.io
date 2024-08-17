/*******************
*Monserad Zamora
********************/
import java.util.*;
import java.util.Scanner;
// Helper method that assists with the tasks needed to be done in the main Guessing Game class
public class GuessingGameHelper{

   // Gets random number and stores in variable num
   public static int getRandomNumber(Random rand){
   // Set num equal to random number 0-100
      int num = rand.nextInt(100)+1;
      //System.out.println(num);
   // return random number
      return num;
   }
   public static boolean getPlayAgain (String prompt){
   // Print the prompt
      System.out.print(prompt);
      try (// Initializes scanner
      Scanner console = new Scanner(System.in)) {
         // Read User input
            String input = console.nextLine();
         // While input is not valid
            while(!(input.equalsIgnoreCase("yes")|| input.equalsIgnoreCase("no"))){
            //Print an error and the prompt again
               System.out.println("Invalid response, must enter \"Yes\" or \"No\"");
               System.out.print(prompt);
               console.nextLine();
            }
         // If input is "yes" then return true to boolean
            return input.equalsIgnoreCase("yes");
      } 
   }
   public static void getInput(int num, String prompt){
   // Create boolean for guessing correctly 
   // set equal to false
      boolean correct = false;
      // Initialize guess count
      int guessCount = 0;
      try (// Create Scanner
      Scanner console = new Scanner(System.in)) {
         // While loop runs until user guesses correctly
         while(!correct){
         //Prints prompt
            System.out.print(prompt);
            // While loop to check if valid input
            while(console.hasNextInt()){
            // User inputs a guess
               int guess = console.nextInt();
            //If guess is correct
               if (guess == num){
            // Guess count is added 1
                  guessCount = guessCount+1;
           // Prompts user that they guessed correctly
                  System.out.println("You got it! It only took you " + guessCount + " attempt(s).");
          // correct is set to true ending loop
                  correct = true;
         // initializes total games
                  int totalGames = 0;
    // total games is added 1
            totalGames = totalGames + 1;
         // While loop calls play again until false
            while(getPlayAgain("Would you like to play again? ")){
    // calls play again
            GuessingGameMain.playGame(); 
         } 
         // Promps user how many games they played
         System.out.println("Great job! You played " + totalGames + " games!"); 
          
               }
               //prompts user if their guess is too high
               else if (guess > num && guess <= 100){
                  System.out.println("Sorry, too high... ");
                  guessCount = guessCount+1;
               
               }
               // prompts user if they guess is too low
               else if(guess < num && guess >= 1){
                  System.out.println("Sorry, too low... ");
                  guessCount = guessCount+1;
               }
               // prompts user if guess is out of scope
               else if(guess <=0 || guess >= 100){
                  System.out.println("Must enter a value between 1 and 100");
               }
            
            }
            // If user inputs a non integer the loop ends and asks them to input integer
            System.out.println("Input must be an integer, please try again");
            console.next();
         }
      }
   
   }

         
}
  





