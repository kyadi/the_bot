import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

interface OnlineAccount {
	int basePrice = 120;
	int regularMoviePrice = 45;
	int exclusiveMoviePrice = 80;
}

class Account implements OnlineAccount, Comparable<Account> {

    int noOfRegularMovies, noOfExclusiveMovies, cost;
    String ownerName;

    // 1) Add a parameterized constructor that initializes the attributes noOfExclusiveMovies and noOfExclusiveMovies.
    public Account(String ownerName,int noOfRegularMovies,int noOfExclusiveMovies){
        this.ownerName = ownerName;
        this.noOfExclusiveMovies = noOfExclusiveMovies;
        this.noOfRegularMovies = noOfRegularMovies;
    }

    // 2. This method returns the monthly cost for the account.
    public int monthlyCost() {
       
       
        int grandPrice =basePrice + noOfRegularMovies*regularMoviePrice + noOfExclusiveMovies*exclusiveMoviePrice;
        return(grandPrice);
        
    }

    // 3. Override the compareTo method of the Comparable interface such that two accounts can be compared based on their monthly cost.


    public int compareTo(Account acc){  
        if(cost==acc.cost)  
        return 0;  
        else if(cost>acc.cost)  
        return 1;  
        else  
        return -1;  
        }  
    
    // 4. Returns "Owner is [ownerName] and monthly cost is [monthlyCost] USD."
    public String toString() {
        String str;
        int cost = monthlyCost();
        str =String.format("Owner is %s and monthly cost is %f USD.",ownerName,cost); 
        

        return(str);

    }
}

// *public class Solution {*/
