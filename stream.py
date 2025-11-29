import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE = os.getenv('API_BASE', 'http://127.0.0.1:8000')

st.set_page_config(page_title='SiteMaster Dashboard', layout='wide')
st.title('SiteMaster — Project ')

menu = st.sidebar.selectbox('Navigation', ['Home', 'Users', 'Products', 'Orders', 'Analytics', 'Run Backup'])


# Home

if menu == 'Home':
    st.write("""Welcome — use the sidebar to navigate.
             SiteMaster, the comprehensive construction management tool that empowers you to take control of your building projects with unparalleled efficiency.
             Whether you're a construction professional, project manager, or contractor, SiteMaster offers a range of features designed to simplify and optimize 
             every aspect of your construction projects.

             Join us as we explore how SiteMaster revolutionizes construction management and helps you achieve superior project control.""")


# Users Management

if menu == 'Users':
    st.header('Users Management')
    col1, col2 = st.columns([2,1])

    # Show existing users
    with col1:
        resp = requests.get(f'{API_BASE}/users')
        users = resp.json()
        df = pd.DataFrame(users)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info('No users found')

    # Add new user
    with col2:
        st.subheader('Add New User')
        name = st.text_input('Name')
        email = st.text_input('Email')
        if st.button('Create User'):
            r = requests.post(f'{API_BASE}/users', json={'name': name, 'email': email})
            if r.status_code in (200,201):
                st.success('User created')
            else:
                st.error(r.text)

# -------------------
# Products Management
# -------------------
if menu == 'Products':
    st.header('Products Management')
    col1, col2 = st.columns([2,1])

    with col1:
        resp = requests.get(f'{API_BASE}/products')
        products = resp.json()
        df = pd.DataFrame(products)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info('No products found')

    with col2:
        st.subheader('Add New Product')
        name = st.text_input('Name')
        category = st.text_input('Category')
        price = st.number_input('Price', min_value=0.0, value=0.0)
        if st.button('Create Product'):
            r = requests.post(f'{API_BASE}/products', json={'name': name, 'category': category, 'price': price})
            if r.status_code in (200,201):
                st.success('Product created')
            else:
                st.error(r.text)

# -------------------
# Orders Management
# -------------------
if menu == 'Orders':
    st.header('Orders Management')
    st.subheader('Place an Order')
    users = requests.get(f'{API_BASE}/users').json()
    products = requests.get(f'{API_BASE}/products').json()
    u_df = pd.DataFrame(users)
    p_df = pd.DataFrame(products)

    if u_df.empty or p_df.empty:
        st.warning('Need at least one user and one product to create an order')
    else:
        user_id = st.selectbox('User', u_df['id'].tolist())
        product_id = st.selectbox('Product', p_df['id'].tolist())
        qty = st.number_input('Quantity', min_value=1, value=1)
        if st.button('Create Order'):
            r = requests.post(f'{API_BASE}/orders', json={'user_id': int(user_id), 'product_id': int(product_id), 'quantity': int(qty)})
            if r.status_code in (200,201):
                st.success('Order created')
            else:
                st.error(r.text)

    st.subheader('All Orders')
    ords = requests.get(f'{API_BASE}/orders').json()
    if ords:
        st.dataframe(pd.DataFrame(ords))
    else:
        st.info('No orders yet')

# -------------------
# Analytics
# -------------------
if menu == 'Analytics':
    st.header('Analytics Dashboard')

    st.subheader('Most Purchased Products')
    resp = requests.get(f'{API_BASE}/analytics/most_purchased')
    if resp.status_code == 200:
        data = resp.json()
        df = pd.DataFrame(data)
        if not df.empty:
            st.bar_chart(df.set_index('product')['total_qty'])
        else:
            st.info('No sales data')
    else:
        st.error('Unable to fetch analytics')

    st.subheader('Top Users')
    resp2 = requests.get(f'{API_BASE}/analytics/top_users')
    if resp2.status_code == 200:
        df2 = pd.DataFrame(resp2.json())
        if not df2.empty:
            st.bar_chart(df2.set_index('user')['total_qty'])
        else:
            st.info('No data')

# -------------------
# Run Backup
# -------------------
if menu == 'Run Backup':
    st.header('Run Database Backup')
    st.write('This will execute the stored procedure `copy_all_data()` to copy data from db_main to db_backup.')

    if st.button('Run Backup Now'):
        try:
            r = requests.post(f'{API_BASE}/run_backup')
            if r.status_code == 200:
                st.success('Backup completed successfully!')
            else:
                st.error(f'Backup failed: {r.text}')
        except Exception as e:
            st.error(str(e))
