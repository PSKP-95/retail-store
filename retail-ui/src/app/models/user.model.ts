export class Address {
    name?: string;
    street?: string;
    village?: string;
    pin?: string;
}

export class User {
    id?: string;
    name?: string;
    email?: string;
    mobNum?: string;
    password?: string;
    address?: Address;
}
