import ProductCard from "@/components/product-card";
import { Product } from "@/types";

export default function ShopPage() {
	const product: Product = {
		id: "",
		name: "Eggs",
		code: "001",
		description:
			"Lorem, ipsum dolor sit amet consectetur adipisicing elit. Dolorem reprehenderit vero expedita dolorum consectetur, accusamus dolores quidem atque? Minima, voluptatibus magni commodi a corrupti fuga itaque harum mollitia libero! Deleniti.",
		category_id: "",
		image: "/static/images/products/eggs.jpg",
		price: 60,
		ratings: 4.5,
		reviews_count: 23,
		stock: 23,
	};

	return <ProductCard product={product} />;
}
