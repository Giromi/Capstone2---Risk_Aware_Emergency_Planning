#!/bin/bash

# 저장할 디렉토리를 지정 (원하는 경로로 변경 가능)
save_dir="proto_files"
mkdir -p "$save_dir"

# 파일 URL 목록
urls=(
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/CommercialBuilding.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/FastFoodRestaurant.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/Carwash.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/Museum.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/Hotel.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/BigGlassTower.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/BuildingUnderConstruction.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/Church.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/GasStation.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/ResidentialTower.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/buildings/protos/LargeResidentialTower.proto"
    "https://raw.githubusercontent.com/cyberbotics/webots/R2023b/projects/objects/traffic/protos/StreetLight.proto"
)

# 모든 파일 다운로드
for url in "${urls[@]}"; do
    file_name=$(basename "$url")
    curl -o "$save_dir/$file_name" "$url"
done

echo "모든 파일 다운로드 완료!"
