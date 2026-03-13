import type { MetadataRoute } from "next";
import { labTests } from "./data/labTests";

const BASE_URL = "https://labrecon.io";

export default function sitemap(): MetadataRoute.Sitemap {
  const testPages: MetadataRoute.Sitemap = labTests
    .filter((t) => !t.bundle)
    .map((t) => ({
      url: `${BASE_URL}/tests/${t.id}`,
      lastModified: t.lastVerified,
      changeFrequency: "monthly",
      priority: 0.8,
    }));

  return [
    {
      url: BASE_URL,
      lastModified: "2026-03-12",
      changeFrequency: "weekly",
      priority: 1.0,
    },
    ...testPages,
  ];
}
