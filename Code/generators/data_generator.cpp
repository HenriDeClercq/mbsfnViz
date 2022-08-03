#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>
#include <random>
#include <vector>

void writeRowToCsv(std::string filename){ 
    // Declarations   
    const std::vector<int>  legal_SF_ALLOC = {1,2,3,4,5,6};
    const std::vector<int>  legal_SF_PERIOD = {1,2,4,8,16,32};
    std::random_device random_ALLOC; 
    std::random_device random_PERIOD;
    std::mt19937 eng_ALLOC(random_ALLOC());
    std::mt19937 eng_PERIOD(random_PERIOD());
    std::uniform_int_distribution<> distr_ALLOC(0, legal_SF_ALLOC.size() - 1);
    std::uniform_int_distribution<> distr_PERIOD(0, legal_SF_PERIOD.size() - 1);

    // Append header
    std::ofstream myFile(filename);
    myFile << "FRAME_ID,FS_ALLOC,FS_PERIOD" << std::endl;
    myFile.close();

    for (int i = 0; i < 100; ++i) {
        std::ofstream myFile(filename, std::ios::app);

        //Construct the new row to append
        int SF_ALLOC = legal_SF_ALLOC[distr_ALLOC(eng_ALLOC)];
        int SF_PERIOD = legal_SF_PERIOD[distr_PERIOD(eng_PERIOD)];
        std::string rowToAppend = std::to_string(i) + "," + std::to_string(SF_ALLOC) + ","  + std::to_string(SF_PERIOD);
        
        std::cout << std::to_string(i) + ": New row appended to file..." << std::endl;
        myFile << rowToAppend << std::endl; 
        std::this_thread::sleep_for(std::chrono::milliseconds(640));  
        myFile.close();
    }
}

int main() {
    writeRowToCsv("mnt/c/Users/Henri/SynShare/Documents/Internships/IDLab_2022/Code/csv_files/random_generated.csv");
    return 0;
}