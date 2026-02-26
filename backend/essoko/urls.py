from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views, views_admin

urlpatterns = [

    # ─────────────────────────────────────
    # AUTH
    # ─────────────────────────────────────
    # POST   /api/auth/register/        — Create account
    # POST   /api/auth/login/           — Get JWT access + refresh token
    # POST   /api/auth/token/refresh/   — Refresh access token
    # POST   /api/auth/logout/          — Blacklist refresh token
    # GET    /api/auth/me/              — Get current user profile
    # PUT    /api/auth/me/              — Update current user profile

    path('auth/register/',         views.RegisterView.as_view(),          name='auth-register'),
    path('auth/login/',            TokenObtainPairView.as_view(),          name='auth-login'),
    path('auth/token/refresh/',    TokenRefreshView.as_view(),             name='auth-token-refresh'),
    path('auth/logout/',           TokenBlacklistView.as_view(),           name='auth-logout'),
    path('auth/me/',               views.MeView.as_view(),                 name='auth-me'),

    # ─────────────────────────────────────
    # FARMER
    # ─────────────────────────────────────
    # GET/PUT  /api/farmers/profile/    — Farmer profile

    path('farmers/profile/',       views.FarmerProfileView.as_view(),      name='farmer-profile'),

    # ─────────────────────────────────────
    # GODOWNS (Public)
    # ─────────────────────────────────────
    # GET  /api/godowns/               — List all active godowns (public)
    # GET  /api/godowns/<id>/          — Single godown detail (public)

    path('godowns/',               views.GodownListView.as_view(),          name='godown-list'),
    path('godowns/<uuid:pk>/',     views.GodownDetailView.as_view(),        name='godown-detail'),

    # ─────────────────────────────────────
    # GODOWNS (Operator manages own)
    # ─────────────────────────────────────
    # GET/POST    /api/godowns/mine/            — List / create own godowns
    # GET/PUT/DEL /api/godowns/mine/<id>/       — Edit / delete a godown

    path('godowns/mine/',                   views.MyGodownView.as_view(),           name='my-godowns'),
    path('godowns/mine/<uuid:pk>/',         views.MyGodownUpdateView.as_view(),     name='my-godown-detail'),

    # ─────────────────────────────────────
    # PRODUCE CATEGORIES
    # ─────────────────────────────────────
    # GET /api/categories/             — All produce categories

    path('categories/',            views.ProduceCategoryListView.as_view(), name='category-list'),

    # ─────────────────────────────────────
    # FARMER DELIVERIES
    # ─────────────────────────────────────
    # GET/POST  /api/deliveries/            — Farmer: list own / create new delivery
    # POST      /api/deliveries/<id>/accept/  — Godown: accept delivery
    # POST      /api/deliveries/<id>/reject/  — Godown: reject delivery
    # GET       /api/godowns/<id>/deliveries/ — Godown: view incoming deliveries

    path('deliveries/',
         views.FarmerDeliveryListCreateView.as_view(),                    name='delivery-list-create'),
    path('deliveries/<uuid:pk>/accept/',
         views.DeliveryAcceptView.as_view(),                              name='delivery-accept'),
    path('deliveries/<uuid:pk>/reject/',
         views.DeliveryRejectView.as_view(),                              name='delivery-reject'),
    path('godowns/<uuid:godown_id>/deliveries/',
         views.GodownIncomingDeliveriesView.as_view(),                    name='godown-deliveries'),

    # ─────────────────────────────────────
    # STOCK LISTINGS
    # ─────────────────────────────────────
    # GET  /api/listings/                       — Public browse all available stock
    # GET  /api/listings/<id>/                  — Public single listing detail
    # GET/POST     /api/godowns/<id>/stock/     — Godown: manage listings
    # GET/PUT/DEL  /api/godowns/<id>/stock/<id>/— Godown: update single listing

    path('listings/',
         views.StockListingPublicView.as_view(),                          name='listing-list'),
    path('listings/<uuid:pk>/',
         views.StockListingDetailView.as_view(),                          name='listing-detail'),
    path('godowns/<uuid:godown_id>/stock/',
         views.GodownStockManageView.as_view(),                           name='godown-stock-list'),
    path('godowns/<uuid:godown_id>/stock/<uuid:pk>/',
         views.GodownStockDetailView.as_view(),                           name='godown-stock-detail'),

    # ─────────────────────────────────────
    # ORDERS
    # ─────────────────────────────────────
    # POST  /api/orders/                    — Consumer: place an order
    # GET   /api/orders/mine/               — Consumer: my order history
    # GET   /api/orders/<id>/               — Order detail (consumer or godown)
    # GET   /api/godowns/<id>/orders/       — Godown: see all incoming orders
    # POST  /api/orders/<id>/<action>/      — Status transition actions:
    #          confirm  — Godown confirms pending order
    #          ready    — Godown marks order ready for pickup
    #          complete — Godown/Transporter marks completed
    #          cancel   — Consumer or Godown cancels order

    path('orders/',
         views.PlaceOrderView.as_view(),                                  name='order-place'),
    path('orders/mine/',
         views.MyOrdersView.as_view(),                                    name='my-orders'),
    path('orders/<uuid:pk>/',
         views.OrderDetailView.as_view(),                                 name='order-detail'),
    path('godowns/<uuid:godown_id>/orders/',
         views.GodownOrdersView.as_view(),                                name='godown-orders'),
    path('orders/<uuid:pk>/<str:action>/',
         views.OrderStatusUpdateView.as_view(),                           name='order-status-update'),

    # ─────────────────────────────────────
    # TRANSPORT
    # ─────────────────────────────────────
    # GET   /api/transport/jobs/              — Transporter: all open jobs
    # GET   /api/transport/jobs/mine/         — Transporter: my assigned jobs
    # POST  /api/transport/jobs/<id>/assign/  — Transporter: take a job
    # POST  /api/transport/jobs/<id>/pickup/  — Transporter: picked up from godown
    # POST  /api/transport/jobs/<id>/deliver/ — Transporter: delivered to consumer

    path('transport/jobs/',
         views.OpenTransportJobsView.as_view(),                           name='transport-jobs'),
    path('transport/jobs/mine/',
         views.MyTransportJobsView.as_view(),                             name='my-transport-jobs'),
    path('transport/jobs/<uuid:pk>/assign/',
         views.AssignTransportJobView.as_view(),                          name='transport-assign'),
    path('transport/jobs/<uuid:pk>/<str:action>/',
         views.UpdateTransportStatusView.as_view(),                       name='transport-update'),

    # ─────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────
    # GET  /api/dashboard/stats/  — Role-based summary stats

    path('dashboard/stats/',
         views.dashboard_stats,                                           name='dashboard-stats'),



    # Admin 
    
    path('admin/stats/',                    views_admin.admin_stats,                    name='admin-stats'),
    path('admin/users/',                    views_admin.AdminUserListView.as_view(),     name='admin-users'),
    path('admin/users/<uuid:pk>/',          views_admin.AdminUserDetailView.as_view(),   name='admin-user-detail'),
    path('admin/users/<uuid:pk>/verify/',   views_admin.AdminVerifyUserView.as_view(),   name='admin-user-verify'),
    path('admin/godowns/',                  views_admin.AdminGodownListView.as_view(),   name='admin-godowns'),
    path('admin/godowns/<uuid:pk>/',        views_admin.AdminGodownDetailView.as_view(), name='admin-godown-detail'),
    path('admin/orders/',                   views_admin.AdminOrderListView.as_view(),    name='admin-orders'),
    path('admin/deliveries/',               views_admin.AdminDeliveryListView.as_view(), name='admin-deliveries'),
    path('admin/listings/',                 views_admin.AdminListingListView.as_view(),  name='admin-listings'),
    path('admin/transport/',                views_admin.AdminTransportListView.as_view(),name='admin-transport'),
    path('admin/categories/',               views_admin.AdminCategoryListCreateView.as_view(), name='admin-categories'),
    path('admin/categories/<int:pk>/',      views_admin.AdminCategoryDetailView.as_view(),     name='admin-category-detail'),


]