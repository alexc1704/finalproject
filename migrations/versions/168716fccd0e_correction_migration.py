"""Initial complete DriftDater schema

Revision ID: 168716fccd0e
Revises:
Create Date: 2026-05-07
"""
from alembic import op
import sqlalchemy as sa

revision = '168716fccd0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('interests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interests_name'), 'interests', ['name'], unique=True)

    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_private', sa.Boolean(), nullable=False),
        sa.Column('is_premium', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('boosted_until', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('likes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('liker_id', sa.Integer(), nullable=False),
        sa.Column('liked_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['liked_id'], ['users.id']),
        sa.ForeignKeyConstraint(['liker_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('liker_id', 'liked_id', name='unique_like_action')
    )
    op.create_index(op.f('ix_likes_liked_id'), 'likes', ['liked_id'], unique=False)
    op.create_index(op.f('ix_likes_liker_id'), 'likes', ['liker_id'], unique=False)

    op.create_table('matches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user1_id', sa.Integer(), nullable=False),
        sa.Column('user2_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user1_id'], ['users.id']),
        sa.ForeignKeyConstraint(['user2_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user1_id', 'user2_id', name='unique_match')
    )
    op.create_index(op.f('ix_matches_user1_id'), 'matches', ['user1_id'], unique=False)
    op.create_index(op.f('ix_matches_user2_id'), 'matches', ['user2_id'], unique=False)

    op.create_table('profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=80), nullable=False),
        sa.Column('last_name', sa.String(length=80), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('gender', sa.String(length=30), nullable=False),
        sa.Column('looking_for', sa.String(length=30), nullable=False),
        sa.Column('bio', sa.Text(), nullable=False),
        sa.Column('location', sa.String(length=120), nullable=False),
        sa.Column('preferred_location', sa.String(length=120), nullable=True),
        sa.Column('min_age', sa.Integer(), nullable=True),
        sa.Column('max_age', sa.Integer(), nullable=True),
        sa.Column('relationship_goal', sa.String(length=80), nullable=True),
        sa.Column('occupation', sa.String(length=120), nullable=True),
        sa.Column('education', sa.String(length=120), nullable=True),
        sa.Column('profile_picture', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_profiles_age'), 'profiles', ['age'], unique=False)
    op.create_index(op.f('ix_profiles_location'), 'profiles', ['location'], unique=False)
    op.create_index(op.f('ix_profiles_user_id'), 'profiles', ['user_id'], unique=False)

    op.create_table('favorites',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'profile_id', name='unique_favorite')
    )
    op.create_index(op.f('ix_favorites_profile_id'), 'favorites', ['profile_id'], unique=False)
    op.create_index(op.f('ix_favorites_user_id'), 'favorites', ['user_id'], unique=False)

    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('match_id', sa.Integer(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('receiver_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['match_id'], ['matches.id']),
        sa.ForeignKeyConstraint(['receiver_id'], ['users.id']),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_created_at'), 'messages', ['created_at'], unique=False)
    op.create_index(op.f('ix_messages_match_id'), 'messages', ['match_id'], unique=False)
    op.create_index(op.f('ix_messages_receiver_id'), 'messages', ['receiver_id'], unique=False)
    op.create_index(op.f('ix_messages_sender_id'), 'messages', ['sender_id'], unique=False)

    op.create_table('profile_interests',
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('interest_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['interest_id'], ['interests.id']),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id']),
        sa.PrimaryKeyConstraint('profile_id', 'interest_id')
    )


def downgrade():
    op.drop_table('profile_interests')
    op.drop_index(op.f('ix_messages_sender_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_receiver_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_match_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_created_at'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_favorites_user_id'), table_name='favorites')
    op.drop_index(op.f('ix_favorites_profile_id'), table_name='favorites')
    op.drop_table('favorites')
    op.drop_index(op.f('ix_profiles_user_id'), table_name='profiles')
    op.drop_index(op.f('ix_profiles_location'), table_name='profiles')
    op.drop_index(op.f('ix_profiles_age'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_matches_user2_id'), table_name='matches')
    op.drop_index(op.f('ix_matches_user1_id'), table_name='matches')
    op.drop_table('matches')
    op.drop_index(op.f('ix_likes_liker_id'), table_name='likes')
    op.drop_index(op.f('ix_likes_liked_id'), table_name='likes')
    op.drop_table('likes')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_interests_name'), table_name='interests')
    op.drop_table('interests')
