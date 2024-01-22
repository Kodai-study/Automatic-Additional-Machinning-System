# -*- coding: utf-8 -*-
import cv2
import numpy as np


def read_image(file_path):
    """画像の読み込み"""
    image = cv2.imread(file_path)
    return image


def convert_to_gray(image):
    """グレースケール変換"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def apply_gaussian_blur(image):
    """ガウシアンブラーを適用して画像を平滑化"""
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred


def apply_canny_edge_detection(image, low_threshold, high_threshold):
    """Cannyエッジ検出を使用してエッジを検出"""
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges


def find_contours(edges):
    """輪郭の検出"""
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, hierarchy


def draw_max_contour(image, contours):
    """最大の輪郭を描画して結果を返す"""
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        contour_image = np.zeros_like(image)
        img = cv2.drawContours(contour_image, [max_contour], -1, (255), 2)
        return img, max_contour
    else:
        print("輪郭が見つかりませんでした。")
        return None, None


def draw_bounding_rectangle(image, contour):
    """輪郭に外接する長方形を描画して寸法を返す"""
    x, y, w, h = cv2.boundingRect(contour)
    rectangle_image = cv2.rectangle(
        image.copy(), (x, y), (x + w, y + h), (0, 255, 0), 2)
    return rectangle_image, w


def save_result_image(image, file_path):
    """結果の画像を保存"""
    cv2.imwrite(file_path, image)


def main():
    file_path = 'ImageInspectionController/test/imgdrill.png'
    image = read_image(file_path)

    gray = convert_to_gray(image)
    blurred = apply_gaussian_blur(gray)
    edges = apply_canny_edge_detection(blurred, 50, 200)
    contours, _ = find_contours(edges)

    result_image, max_contour = draw_max_contour(gray, contours)
    if result_image is not None:
        save_result_image(
            result_image, 'ImageInspectionController/test/contour_result.png')

        rectangle_image, x_dimension = draw_bounding_rectangle(
            image, max_contour)
        if rectangle_image is not None:
            save_result_image(
                rectangle_image, 'ImageInspectionController/test/rectangle_result.png')
            print(f'X方向の寸法: {x_dimension}')
        else:
            print("長方形が検出されませんでした。")

    cv2.imshow('Original Image', image)
    cv2.imshow('Blurred Image', blurred)
    cv2.imshow('Canny Edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
