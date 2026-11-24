const products = [
  { id:1, name:'Sculptural Oak Chair', maker:'North & Form', price:289, category:'Home', badge:'Bestseller', image:'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=800&q=85' },
  { id:2, name:'Handwoven Linen Tote', maker:'Tala Workshop', price:68, category:'Fashion', badge:'New', image:'https://images.unsplash.com/photo-1559563458-527698bf5295?auto=format&fit=crop&w=800&q=85' },
  { id:3, name:'Sandstone Serving Bowl', maker:'Atelier Noma', price:54, category:'Ceramics', badge:'', image:'https://images.unsplash.com/photo-1610701596061-2ecf227e85b2?auto=format&fit=crop&w=800&q=85' },
  { id:4, name:'Botanical Ritual Set', maker:'Still & Wild', price:42, category:'Wellness', badge:'Limited', image:'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=800&q=85' },
  { id:5, name:'Soft Wool Throw', maker:'Morrow Studio', price:118, category:'Home', badge:'', image:'https://images.unsplash.com/photo-1583845112203-29329902332e?auto=format&fit=crop&w=800&q=85' },
  { id:6, name:'Woven Leather Clogs', maker:'Sol & Sole', price:146, category:'Fashion', badge:'New', image:'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=85' },
  { id:7, name:'Speckled Tea Cups', maker:'Common Clay', price:76, category:'Ceramics', badge:'Set of 4', image:'https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?auto=format&fit=crop&w=800&q=85' },
  { id:8, name:'Hinoki Body Oil', maker:'Still & Wild', price:36, category:'Wellness', badge:'', image:'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=800&q=85' }
];

const grid = document.getElementById('productGrid');
const cart = [];

function productCard(p){
  return `<article class="product-card">
    <div class="product-image">
      <img src="${p.image}" alt="${p.name}" loading="lazy">
      ${p.badge ? `<span class="product-badge">${p.badge}</span>` : ''}
      <button class="quick-add" data-add="${p.id}" aria-label="Add ${p.name} to bag">+</button>
    </div>
    <div class="product-info">
      <span class="product-maker">${p.maker}</span>
      <div class="product-name-row"><h3>${p.name}</h3><strong>$${p.price}</strong></div>
    </div>
  </article>`;
}

function renderProducts(items=products){ grid.innerHTML = items.map(productCard).join(''); }
renderProducts();

function showToast(message){
  const toast=document.getElementById('toast'); toast.textContent=message; toast.classList.add('show');
  setTimeout(()=>toast.classList.remove('show'),2200);
}

grid.addEventListener('click',e=>{
  const button=e.target.closest('[data-add]');
  if(!button)return;
  const product=products.find(p=>p.id===Number(button.dataset.add));
  const found=cart.find(item=>item.id===product.id);
  if(found)found.qty++; else cart.push({...product,qty:1});
  updateCart(); showToast(`${product.name} added to your bag`);
});

function updateCart(){
  document.getElementById('cartCount').textContent=cart.reduce((sum,item)=>sum+item.qty,0);
  const items=document.getElementById('cartItems');
  if(!cart.length){items.innerHTML='<div class="empty-cart">Your bag is waiting for something beautiful.</div>';} else {
    items.innerHTML=cart.map(item=>`<div class="cart-item">
      <img src="${item.image}" alt="${item.name}">
      <div><span class="product-maker">${item.maker}</span><h3>${item.name}</h3>
        <div class="qty-controls"><button data-minus="${item.id}">−</button><span>${item.qty}</span><button data-plus="${item.id}">+</button></div>
      </div><strong>$${item.price*item.qty}</strong>
    </div>`).join('');
  }
  document.getElementById('cartSubtotal').textContent='$'+cart.reduce((sum,item)=>sum+item.price*item.qty,0);
}

document.getElementById('cartItems').addEventListener('click',e=>{
  const plus=e.target.closest('[data-plus]'); const minus=e.target.closest('[data-minus]');
  const id=plus?.dataset.plus || minus?.dataset.minus; if(!id)return;
  const item=cart.find(p=>p.id===Number(id));
  if(plus)item.qty++; else if(--item.qty<=0)cart.splice(cart.indexOf(item),1);
  updateCart();
});

const drawer=document.getElementById('cartDrawer'),overlay=document.getElementById('overlay');
function toggleCart(open){drawer.classList.toggle('open',open);overlay.classList.toggle('open',open);drawer.setAttribute('aria-hidden',String(!open));}
document.getElementById('cartButton').addEventListener('click',()=>toggleCart(true));
document.getElementById('closeCart').addEventListener('click',()=>toggleCart(false));
overlay.addEventListener('click',()=>toggleCart(false));

document.getElementById('searchToggle').addEventListener('click',()=>{
  const panel=document.getElementById('searchPanel'); panel.classList.toggle('open');
  if(panel.classList.contains('open'))document.getElementById('searchInput').focus();
});
document.getElementById('searchInput').addEventListener('input',e=>{
  const q=e.target.value.toLowerCase(); renderProducts(products.filter(p=>(p.name+' '+p.maker+' '+p.category).toLowerCase().includes(q)));
});

document.querySelectorAll('[data-category]').forEach(card=>card.addEventListener('click',()=>{
  const category=card.dataset.category; renderProducts(products.filter(p=>p.category===category));
  document.getElementById('products').scrollIntoView({behavior:'smooth'});
}));
document.getElementById('showAll').addEventListener('click',()=>renderProducts());

document.getElementById('categoryNext').addEventListener('click',()=>{const g=document.getElementById('categoryGrid');g.append(g.firstElementChild)});
document.getElementById('categoryPrev').addEventListener('click',()=>{const g=document.getElementById('categoryGrid');g.prepend(g.lastElementChild)});

const sellerModal=document.getElementById('sellerModal');
document.getElementById('sellerButton').addEventListener('click',()=>sellerModal.showModal());
document.getElementById('closeSeller').addEventListener('click',()=>sellerModal.close());
document.getElementById('sellerForm').addEventListener('submit',e=>{e.preventDefault();sellerModal.close();showToast('Application received — welcome to Mera!');e.target.reset();});

document.getElementById('checkoutButton').addEventListener('click',()=>{
  if(!cart.length){showToast('Your bag is empty');return;}showToast('Secure checkout ready');toggleCart(false);
});
