export class Item {
    id!: string;
    name!: string;
    description!: string;
    price!: number;
    originalPrice!: number;
    stock!: number;
    unit!: string;
    imageUrl!: string;
    tags!: string[];
}

export class CartItem {
    iid!: string;
    qty!: number;
}

export class Cart {
    items!: CartItem[];
}