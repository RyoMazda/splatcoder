#include <iostream>
#include <stdexcept>
#include <cassert>
#include <cmath>
#include <vector>
#include <string>
using namespace std;


int main() {
  int N;
  cin >> N;

  assert(0 <= N && N <= 10000);
  cout << N << endl;
  return 0;
}
