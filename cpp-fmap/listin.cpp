#include <Freeze/Freeze.h>
#include <Ice/Application.h>
#include "ListinMap.h"

class App : public Ice::Application {
public:
    int run(int argc, char* argv[]) {
	Freeze::ConnectionPtr conn = Freeze::createConnection(communicator(), "db");
	ListinMap map(conn, "listin", true);

	if (argc < 2) {
	    for (ListinMap::iterator i = map.begin(); i != map.end(); ++i) {
		std::cout << i->second->nombre << "\t"
			  << i->second->telefono << std::endl;
	    }
	}
	else if (0 == ::strcmp(argv[1], "add")) {
	    map.insert(std::make_pair(argv[2], 
				      new Listin::Registro(argv[3], 
							   argv[2])));
	}
	else if (0 == ::strcmp(argv[1], "del")) {
	    map.erase(map.find(argv[2]));
	}
	else if (0 == ::strcmp(argv[1], "nombre")) {
	    ListinMap::iterator i = map.find(argv[2]);
	    if (i != map.end()) {
		std::cout << i->second->nombre << "\t"
			  << i->second->telefono << std::endl;
	    }
	}
	else if (0 == ::strcmp(argv[1], "telefono")) {
	    ListinMap::iterator i = map.findByTelefono(argv[2]);
	    if (i != map.end()) {
		std::cout << i->second->nombre << "\t"
			  << i->second->telefono << std::endl;
	    }
	}
    }
};

int
main(int argc, char* argv[])
{
    App app;
    app.main(argc, argv);
}
