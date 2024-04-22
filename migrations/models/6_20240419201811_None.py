from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(32) NOT NULL  DEFAULT 'Нет имени',
    `hashed_password` VARCHAR(256) NOT NULL,
    `role` VARCHAR(128) NOT NULL  DEFAULT 'user',
    `description` VARCHAR(512) NOT NULL  DEFAULT 'Привет! Это мой блог...',
    `avatar_link` VARCHAR(1024) NOT NULL,
    `post_amount` INT NOT NULL,
    `disabled` BOOL NOT NULL  DEFAULT 0,
    `is_admin` BOOL NOT NULL  DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `post` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(128) NOT NULL,
    `text` VARCHAR(10240) NOT NULL,
    `preview_link` VARCHAR(1024) NOT NULL,
    `tags` JSON NOT NULL,
    `time_to_read` VARCHAR(256) NOT NULL,
    `post_rating` INT NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `edited_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `created_by_id` INT NOT NULL,
    CONSTRAINT `fk_post_user_11c6bcdd` FOREIGN KEY (`created_by_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `comment` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `text` VARCHAR(256) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `edited_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `created_by_id` INT NOT NULL,
    `post_id` INT NOT NULL,
    CONSTRAINT `fk_comment_user_f9e42874` FOREIGN KEY (`created_by_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_comment_post_eff1916f` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
