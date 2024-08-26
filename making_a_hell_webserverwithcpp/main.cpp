#include "httplib.h"
#include <opencv2/opencv.hpp> 
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <vector>

//g++ -o server main.cpp -I/usr/include/opencv4 -lopencv_core -lopencv_imgproc -lopencv_imgcodecs -lssl -lcrypto

int main() {
    httplib::Server svr;

    svr.Get("/get", [](const httplib::Request &req, httplib::Response &res) {
        res.set_content("is a good service", "text/plain");
    });

    svr.Post("/upload", [](const httplib::Request &req, httplib::Response &res) {
        auto it = req.files.find("image");

        if (it != req.files.end()) {
            const auto& file = it->second;

            std::vector<uchar> img_data(file.content.begin(), file.content.end());
            cv::Mat img = cv::imdecode(img_data, cv::IMREAD_COLOR);
            if (img.empty()) {
                res.status = 500;
                res.set_content("Failed to load the image!", "text/plain");
                return;
            }

            cv::Mat gray_img;
            cv::cvtColor(img, gray_img, cv::COLOR_BGR2GRAY);

            std::vector<uchar> gray_img_encoded;
            std::vector<int> params = {cv::IMWRITE_PNG_COMPRESSION, 9}; 
            cv::imencode(".png", gray_img, gray_img_encoded, params);

            std::string gray_img_str(gray_img_encoded.begin(), gray_img_encoded.end());

            res.set_content(gray_img_str, "image/png");
        } else {
            res.status = 400;
            res.set_content("Image upload failed!", "text/plain");
        }
    });

    svr.listen("0.0.0.0", 80);
}
