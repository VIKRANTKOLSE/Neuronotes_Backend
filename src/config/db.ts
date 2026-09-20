import {Pool} from "pg";

const userPool=new Pool({
    host:"localhost",
    port:5432,
    user:"ravik",
    password:"vicky@9999",
    database:"neuronotes_testing",
    max:20
});

export default userPool;