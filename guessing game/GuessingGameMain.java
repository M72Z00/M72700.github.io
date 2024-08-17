/*******************
*Monserad Zamora
********************/
import java.util.*;
import java.util.Scanner;
// Controls the flow of the application and user interaction
public class GuessingGameMain{
   public static void main(String[] args) {
   // Create Scanner 
      Scanner console = new Scanner(System.in);
  // Call runProgram form Helper class
      runProgram();
   }
   
   public static void runProgram(){
   // Calls play game
      playGame();
   }
   public static void playGame(){
    // Create Random Object
      Random rand = new Random();
    
   // Create variable num and set equal to getRandomNumber
      int num = GuessingGameHelper.getRandomNumber(rand);
   // Call getInput(num,prompt)
      GuessingGameHelper.getInput(num,"Enter a number between 1 and 100: ");
   }
   
   
}
