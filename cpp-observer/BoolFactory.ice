module IBool {
    interface RWRemoteFactory {
        Object* create();
        void destroy(Object* obj);
    };
};
