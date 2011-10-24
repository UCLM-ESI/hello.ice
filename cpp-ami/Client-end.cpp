// -*- coding:utf-8; tab-width:4; mode:cpp -*-

#include <Ice/Ice.h>
#include <factorial.h>

using namespace Ice;
using namespace std;

class Client: public Ice::Application {
  int run(int argc, char* argv[]) {

    ObjectPrx obj = communicator()->stringToProxy(argv[1]);
    UCLM::MathPrx prx = UCLM::MathPrx::checkedCast(obj);

	Ice::AsyncResultPtr async_result = prx->begin_factorial(atoi(argv[2]));
	cout << "this was async call" << endl;

	cout << prx->end_factorial(async_result) << endl;

    return 0;
  }
};


int main(int argc, char* argv[]) {
  if (argc != 3) {
	cerr << "usage: " << argv[0] << "<server> <value>" << endl;
	return 1;
  }

  Ice::Application* app = new Client();
  return app->main(argc, argv);
}
