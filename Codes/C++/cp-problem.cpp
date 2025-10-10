//For each test case, output on a new line, the number of eligible voters.

#include <iostream>
using namespace std;
int main(){
    int t;
    cin>>t;
    while(t--){//loop runs t times
        int n,x;
        cin>>n>>x;//n is number of people,x is min age of a person to vote
        int age[n]; int count=0;//array of size n
        for(int i=0; i<n; i++){
            cin>>age[i];
            if(x<=age[i])
            count++;//count stores the number pf eligible voters
        }
        cout<<count<<endl;
    }
    return 0;
}
