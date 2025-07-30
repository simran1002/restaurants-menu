from typing import List, Dict, Union


def calculate_total_revenue(orders: List[Dict[str, Union[str, int, float]]]) -> float:
    
    if not orders:
        return 0.0
    
    if not isinstance(orders, list):
        raise TypeError("Orders must be a list")
    
    total_revenue = 0.0
    
    for i, order in enumerate(orders):
        if not isinstance(order, dict):
            raise TypeError(f"Order at index {i} must be a dictionary")
        
       
        required_fields = ['item_name', 'quantity', 'price_per_item']
        missing_fields = [field for field in required_fields if field not in order]
        if missing_fields:
            raise ValueError(f"Order at index {i} missing required fields: {missing_fields}")
        
       
        item_name = order['item_name']
        quantity = order['quantity']
        price_per_item = order['price_per_item']
        
      
        if not isinstance(item_name, str) or not item_name.strip():
            raise ValueError(f"Order at index {i}: item_name must be a non-empty string")
        
       
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError(f"Order at index {i}: quantity cannot be negative")
        except (ValueError, TypeError):
            raise ValueError(f"Order at index {i}: quantity must be a non-negative integer")
        
        
        try:
            price_per_item = float(price_per_item)
            if price_per_item < 0:
                raise ValueError(f"Order at index {i}: price_per_item cannot be negative")
        except (ValueError, TypeError):
            raise ValueError(f"Order at index {i}: price_per_item must be a non-negative number")
        
        
        order_revenue = quantity * price_per_item
        total_revenue += order_revenue
    
    return round(total_revenue, 2)


def get_data() -> float:
   
    sample_orders = [
        {'item_name': 'Margherita Pizza', 'quantity': 2, 'price_per_item': 15.99},
        {'item_name': 'Caesar Salad', 'quantity': 1, 'price_per_item': 12.50},
        {'item_name': 'Garlic Bread', 'quantity': 3, 'price_per_item': 4.25},
        {'item_name': 'Soda', 'quantity': 4, 'price_per_item': 2.99}
    ]
    
    return calculate_total_revenue(sample_orders)


def validate_order_format(order: Dict) -> bool:
   
    required_fields = ['item_name', 'quantity', 'price_per_item']
    return all(field in order for field in required_fields)


def get_order_summary(orders: List[Dict]) -> Dict:
   
    if not orders:
        return {
            'total_revenue': 0.0,
            'total_items': 0,
            'total_orders': 0,
            'average_order_value': 0.0
        }
    
    total_revenue = calculate_total_revenue(orders)
    total_items = sum(order['quantity'] for order in orders)
    total_orders = len(orders)
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    
    return {
        'total_revenue': total_revenue,
        'total_items': total_items,
        'total_orders': total_orders,
        'average_order_value': round(average_order_value, 2)
    }


if __name__ == "__main__":
    print("Testing calculate_total_revenue function:")
    
    test_orders = [
        {'item_name': 'Pizza', 'quantity': 2, 'price_per_item': 15.99},
        {'item_name': 'Burger', 'quantity': 1, 'price_per_item': 8.50}
    ]
    print(f"Test 1 - Normal case: ${calculate_total_revenue(test_orders)}")
    
    print(f"Test 2 - Empty list: ${calculate_total_revenue([])}")
    
    single_order = [{'item_name': 'Coffee', 'quantity': 1, 'price_per_item': 3.50}]
    print(f"Test 3 - Single order: ${calculate_total_revenue(single_order)}")
    
    zero_quantity = [{'item_name': 'Free Sample', 'quantity': 0, 'price_per_item': 10.00}]
    print(f"Test 4 - Zero quantity: ${calculate_total_revenue(zero_quantity)}")
    
    print(f"\nOrder Summary: {get_order_summary(test_orders)}")