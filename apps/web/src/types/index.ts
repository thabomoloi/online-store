export interface Product {
	id: string;
	code: string;
	name: string;
	description: string;
	image: string;
	price: number;
	stock: number;
	category_id: string;
	ratings: number;
	reviews_count: number;
}

export interface Category {
	id: string;
	name: string;
}

export interface Review {
	id: string;
	rating: number;
	comment: string;
	data: string;
	product_id: string;
	user_id: string;
}
