from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create user
user1 = User(name="Alan Po-Ching Yang", email="alankashiwa@gmail.com",
             picture="https://lh3.googleusercontent.com/-RQlWwB6D5_s/AAAAAAAAAAI/AAAAAAAAAE8/PnzGBNmOHT0/photo.jpg") # NOQA
session.add(user1)
session.commit()

# Coffee items
category1 = Category(name="coffee")
session.add(category1)
session.commit()

item1 = Item(
    user_id=1,
    name="drip",
    image_url="https://upload.wikimedia.org/wikipedia/commons/c/c2/Nel_Drip_Coffee.jpg", # NOQA
    description=("Drip-brewed, or filtered, coffee is brewed by hot "
                 "water passing slowly over roasted, ground coffee "
                 "beans contained in a filter."
    ),
    price="$2.95",
    category=category1
)
session.add(item1)
session.commit()

item2 = Item(
    user_id=1,
    name="latte",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Caffe_latte_%286730936643%29.jpg/1920px-Caffe_latte_%286730936643%29.jpg", # NOQA
    description=("A latte is an espresso and steamed milk,　generally "
                 "in a 1:3 to 1:5 ratio of espresso to milk, with a "
                 "little foam on top."
    ),
    price="$3.70",
    category=category1
)
session.add(item2)
session.commit()

item3 = Item(
    user_id=1,
    name="cappuccino",
    image_url="https://upload.wikimedia.org/wikipedia/commons/3/3e/Cappuccino_rossoblu.jpg", # NOQA
    description=("Cappuccino is a coffee-based drink prepared with "
                 "espresso, hot milk, and steamed milk foam."
    ),
    price="$3.65",
    category=category1
)
session.add(item3)
session.commit()

item4 = Item(
    user_id=1,
    name="macchiato",
    image_url="https://upload.wikimedia.org/wikipedia/commons/0/08/Macchiato_as_being_served_at_Kaffebrenneriet_Torshov%2C_Oslo%2C_Norway_2_600x600_100KB.jpg", # NOQA
    description=("Macchiato, meaning 'stained', is an espresso with "
                 "a dash of foamed milk."
    ),
    price="$3.95",
    category=category1
)
session.add(item4)
session.commit()

item5 = Item(
    user_id=1,
    name="mocha",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Mocaccino-Coffee.jpg/1920px-Mocaccino-Coffee.jpg", # NOQA
    description=("A caffè mocha, also called mocaccino, is a "
                 "chocolate-flavored variant of a caffè latte."
    ),
    price="$3.80",
    category=category1
)
session.add(item5)
session.commit()

item6 = Item(
    user_id=1,
    name="americano",
    image_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Espresso_Americano.jpeg", # NOQA
    description=("Americano is a style of coffee prepared by brewing "
                 "espresso with added hot water, giving it a similar "
                 "strength to, but different flavor from drip coffee."
    ),
    price="$3.80",
    category=category1
)
session.add(item6)
session.commit()

# Tea items
category2 = Category(name="tea")
session.add(category2)
session.commit()

item7 = Item(
    user_id=1,
    name="darjeeling",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Nice_Cup_of_Black_Tea.jpg/1920px-Nice_Cup_of_Black_Tea.jpg", # NOQA
    description=("Darjeeling tea is a tea from the Darjeeling district "
                 "in West Bengal, India. It is available in black, green, "
                 "white and oolong."
    ),
    price="$3.15",
    category=category2
)
session.add(item7)
session.commit()

item8 = Item(
    user_id=1,
    name="green tea",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Gr%C3%B8n_te_%286290842532%29.jpg/1920px-Gr%C3%B8n_te_%286290842532%29.jpg", # NOQA
    description=("Green tea is a type of tea that is made from Camellia "
                 "sinensis leaves that have not undergone the same withering "
                 "and oxidation process used to make oolong and black tea."
    ),
    price="$3.00",
    category=category2
)
session.add(item8)
session.commit()

# Food items
category3 = Category(name="food")
session.add(category3)
session.commit()

item9 = Item(
    user_id=1,
    name="tiramisu",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Tiramisu_with_blueberries_and_raspberries%2C_July_2011.jpg/1920px-Tiramisu_with_blueberries_and_raspberries%2C_July_2011.jpg", # NOQA
    description=("Tiramisu is a popular coffee-flavoured italian cuisine "
                 "custard dessert. It is made of ladyfingers dipped in "
                 "coffee, layered with a whipped mixture of eggs, sugar, "
                 "and mascarpone cheese, flavoured with cocoa."
    ),
    price="$4.00",
    category=category3
)
session.add(item9)
session.commit()

item10 = Item(
    user_id=1,
    name="shortcake",
    image_url="https://upload.wikimedia.org/wikipedia/commons/4/43/Strawberry_shortcake.jpg", # NOQA
    description=("Shortcake is typically made with flour, sugar, "
                 "baking powder or soda, salt, butter, milk or cream, "
                 "and sometimes eggs. The dry ingredients are blended, "
                 "and then the butter is cut in until the mixture resembles "
                 "cornmeal."
    ),
    price="$3.90",
    category=category3
)
session.add(item10)
session.commit()

item11 = Item(
    user_id=1,
    name="brownie",
    image_url="https://upload.wikimedia.org/wikipedia/commons/2/25/Brownie_Neum%C3%BCller_Ferdinand_cropped.jpg", # NOQA
    description=("A brownie is a square, baked, chocolate dessert. "
                 "Brownies come in a variety of forms and may be either "
                 "fudgy or cakey, depending on their density. They may "
                 "include nuts, frosting, cream cheese, chocolate chips, "
                 "or other ingredients."
    ),
    price="$3.75",
    category=category3
)
session.add(item11)
session.commit()

# Drinkware items
category4 = Category(name="drinkware")
session.add(category4)
session.commit()

item12 = Item(
    user_id=1,
    name="coffee cup",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/2006-10-15_Bob01.jpg/1024px-2006-10-15_Bob01.jpg", # NOQA
    description=("A coffee cup is a container that coffee and "
                 "espresso-based drinks are served in. Coffee cups are "
                 "typically made of glazed ceramic, and have a single "
                 "handle for portability while the beverage is hot."
    ),
    price="$8.50",
    category=category4
)
session.add(item12)
session.commit()

item13 = Item(
    user_id=1,
    name="tea cup",
    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Small_black_and_green_CUP_no_handle.JPG/1920px-Small_black_and_green_CUP_no_handle.JPG", # NOQA
    description=("A teacup is a cup, with or without a handle, generally "
                 "a small one that may be grasped with the thumb and one "
                 "or two fingers."
    ),
    price="$6.50",
    category=category4
)
session.add(item13)
session.commit()
