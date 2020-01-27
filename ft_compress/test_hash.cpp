#include<iostream>  
#include<string>
 #include <stdint.h>  
using namespace std; 
  
// main function - 
// where the execution of program begins 
//int main() 
//{ 
//    // prints hello world 
//    cout<<"Hello World"; 
      
//    return 0; 
//} 


uint32_t hash(const std::string& str){
  uint32_t h = 2166136261;
  for (size_t i = 0; i < str.size(); i++) {

    cout<<str[i]<<":"<<+int8_t(str[i])<<":"<<uint32_t(int8_t(str[i]))<<endl;
    h = h ^ uint32_t(int8_t(str[i]));
    h = h * 16777619;
    cout <<"h: "<<h<<endl;
  }
  return h%2000000+602;
}



int main(){
	std::string in;
        getline(cin, in);
        cout<<hash(in);
}
