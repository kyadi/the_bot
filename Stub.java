



class SerialMultiplier {

    int first = 1;
    int second = 1; 
    int third = 1; 
    int forth = 1; 
    int fifth = 1;
    long result;

    // 1) Add a parameterized constructor that initializes the attributes noOfExclusiveMovies and noOfExclusiveMovies.
    public SerialMultiplier(int first,int second,int third, int forth, int fifth){
        this.first = first;
        this.second = second;
        this.third = third;
        this.forth = forth;
        this.fifth = fifth;
    }

    public SerialMultiplier(int first,int second,int third, int forth){
        this.first = first;
        this.second = second;
        this.third = third;
        this.forth = forth;
        
    }

    public SerialMultiplier(int first,int second,int third){
        this.first = first;
        this.second = second;
        this.third = third;
        
    }
    public SerialMultiplier(int first,int second){
        this.first = first;
        this.second = second;
        
    }
    public SerialMultiplier(int first){
        this.first = first;
        
        
    }
    public SerialMultiplier(){     
        
    }

    
    public long multiplier() {
        this.result = first*second*third*forth*fifth;
       
       
        
        return(result);
        
    }
}


    class Stub extends SerialMultiplier {
       
        public void SerialMultiplier(int first,int second,int third, int forth, int fifth){
            this.first = first;
            this.second = second;
            this.third = third;
            this.forth = forth;
            this.fifth = fifth;
        }
    
        public void SerialMultiplier(int first,int second,int third, int forth){
            this.first = first;
            this.second = second;
            this.third = third;
            this.forth = forth;
            
        }
    
        public void SerialMultiplier(int first,int second,int third){
            this.first = first;
            this.second = second;
            this.third = third;
            
        }
        public void SerialMultiplier(int first,int second){
            this.first = first;
            this.second = second;
            
        }
        public void SerialMultiplier(int first){
            this.first = first;
            
            
        }
        public void SerialMultiplier(){     
            
        }
    
       
       
       
        @Override
        public long multiplier() {
            this.result = first*second*third*forth*fifth;
           
           
            
            return(result);
        }

        public static void main(String args[]){
            SerialMultiplier sm = new SerialMultiplier(5,2);
            sm.multiplier();
            
            }
    }

    

   